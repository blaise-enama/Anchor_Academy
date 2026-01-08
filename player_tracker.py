import os
import mysql.connector
import pymysql
import csv
import logging
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def connect_to_database():
    load_dotenv()   # Loads .env file

    host_name = os.getenv("DB_HOST")
    user_name = os.getenv("DB_USER")
    user_password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "pymysql")

    conn = None
    try:
        if driver == 'mysql-connector':
            conn = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd= user_password,
                db= database
            )
        elif driver == 'pymysql':
            conn = pymysql.connect(
                host=host_name,
                user=user_name,
                passwd= user_password,
                db= database
            )
        else:
            raise ValueError("Unsupported driver. Use 'mysql-connector' or 'pymysql'.")
        
        logging.info("MySQL Database connection successful!") 
    
    except Exception as e:
        logging.info(f"Error while connecting to MySQL: {e}")
        conn = None

    return conn


def execute_query(conn,query, params=None, fetch=False):
    """
    Execute a query safely using an existing pymysql connection

    Args:
        conn (pymysql.connections.Connection): Active MySQL connection object
        query (str): SQL query to be executed.
        params (tuple, optional) Parameters for parameterized queries 
        fetch (bool): If True, fetch results (for SELECT queries). Otherwise, commit. 
    
    do i need this function if I can just run cursor.execute("SELECT...;")
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                logging.info("SELECT query executed")
                return cursor.fetchall()
            else:
                conn.commit()
                logging.info("query successfully executed")
                return None

    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None


def get_mysql_csv(table):
    """
    A function that pulls a mysql table into a csv file using pandas' read_sql method
    After establishing a connection

    Parameters:
    table: the name of the mysql table that is to be specified upon calling the function
    """
    try:
        #Create a database engine
        db_connection_str = 'mysql+pymysql://root:Enamfam.7@localhost/Anchor_academy'
        db_connection = create_engine(db_connection_str)

        #Define the table and output CSV file
        table_name = table      # "roster"
        output_csv_file = "players_data.csv"

        #read data from MySQL into a pandas Dataframe
        df = pd.read_sql(f"SELECT * FROM {table_name}", db_connection)

        #Export DataFrame to CSV
        df.to_csv(output_csv_file, index=False) # index = False prevents writing DataFrame index as a column
        print(f"Data from '{table_name}' exported to '{output_csv_file}' successfully using pandas.")

    except Exception as e:
        print(f"Error: {e}")


class Player:
    #initialize attributes of the player object
    def __init__(self, player_id, name, position, age, team=None):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.age = age 
        self.team = team
        self.sessions = [] # stores multiple Sessions objects


    def add_session(self, session):
        self.sessions.append(session)


    def save_to_db(self,conn):
        cursor = conn.cursor() # establish a connection with the server
        cursor.execute("""
            INSERT INTO roster ( name, position, age, team) 
            VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE name=%s, position=%s, age=%s
        """,(self.player_id, self.name, self.position, self.age, self.team)
        )

        #save session data
        for s in self.sessions:
            cursor.execute("""
                INSERT INTO sessions (player_id, session_date, total_distance, sprint_count, top_speed,
                                       touches_left, touches_right, acceleration_events, deceleration_events,
                                       session_duration, fatigue_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.player_id, s.session_date, s.distance, s.sprints, s.top_speed,
                  s.touches_left, s.touches_right, s.accels, s.decels, s.duration, s.fatigue))
        conn.commit()
        #player_id = cursor.lastrowid







class Session:
    def __init__(self, player_id, session_date, duration, distance, sprint_count, max_speed, touches_left, touches_right):
        self.player_id = player_id
        self.session_date = session_date
        self.distance = distance
        self.duration = duration
        self.sprints = sprint_count
        self.max_speed = max_speed
        self.touches_left = touches_left
        self.touches_right = touches_right
        self.sessions = []

    def load_sessions_from_csv(file_path, player_id, conn):
        """
        this is a loader function that reads the file exported from the Playermaker tracker, creates a Session object for each record, 
        and savees it to the database. 

        Now one function call (load_sessions_from_csv("messi_august.csv", 1, conn)) updates all of Messis sessions automatically.
        """
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                session = Session(
                    session_id=int(row["session_id"]),
                    player_id=player_id,
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    duration=int(row["duration"]),
                    distance_covered=float(row["distance_covered"])
                )
                session.save_to_db(conn)

    
    def foot_usage_ratio(self):
        """
        a method for determining the ratio of touches between left and right 
        """
        
        #combine left and right touches for a comined total
        total_touches = self.touches_left + self.touches_right

        #return the ratio 
        r_foot_ratio= self.touches_right / total_touches 
        l_foot_ratio= self.touches_left / total_touches

        #return a tuple of right to left ratios
        return (r_foot_ratio,l_foot_ratio)

        
    def work_rate(self):
        """
        a method for determining the work rate of a player for each session
        """
        pass

    def mysql_to_csv(self, conn):
        #A function to pull a mysql table into a csv using mysql.connector and csv (for pandas usage/ visualization?)
        """
        takes conn, an established mysql database connection, and executes a command to fetch all data from a given table

        """
        try:
            mysql_cursor = conn.cursor()

            #Define the table and output CSV file
            table_name = "sessions"
            output_csv_file = "sessions_data.csv"

            #Execute query to fetch data
            mysql_cursor.execute(f"SELECT * FROM {table_name}")

            # Get column names for the header
            column_names = [i[0] for i in mysql_cursor.description]

            #fetch all rows
            rows = mysql_cursor.fetchall()

            #write data into a CSV
            with open(output_csv_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(column_names)  # writes header
                csv_writer.writerows(rows)  # write data rows
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'conn' in locals() and conn.is_connected():
                mysql_cursor.close()
                conn.close()


    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Anchor_Academy.sessions (player_id, date, duration, distance, sprint_count, max_speed, touches_left, touches_right) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE date=%s, duration=%s, distance=%s, sprint_count=%s, max_speed=%s, touches_left=%s, touches_right=%s
        """,
            (self.player_id, self.session_date, self.duration, self.distance, self.sprints, self.max_speed, self.touches_left, self.touches_right)
        )

        conn.commit() #Commits current transaction.This method sends a COMMIT statement to the MySQL server, committing the current transaction.        conn.close()






class PlayerRepository:
    """
    This is a Repository class designed to manage the player table
    """
    def __init__(self, conneciton):
        self.connection = conneciton


    def add_player(self, player):
        """
        adds an existing player object to the repository 
        """
        query = """
        INSERT INTO roster (name, position, age, team)
        VALUES %s,%s,%s,%s);
        """
        logging.info(f"query: {query}")
        logging.info(f"query count: {query.count("%s")}")

        execute_query(self.connection, query, (player.name, player.position, player.age, player.team))
        #self.conn.commit()

    def get_roster(self):
        query = "SELECT * FROM roster"
        return execute_query(self.connection, query, fetch=True)
    
    def delete_player(self, player_name):
        query= "DELETE FROM roster WHERE name = %s"
        execute_query(self.connection, query)
        logging.info(f"Successfully deleted player {player_name} from the database")

    
    def locate_player(self,player_name):
        """Locates a given player by name 
        
        """
        query = "SELECT * FROM roster WHERE name = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (player_name))
            return cursor.fetchone()
        #execute_query(self.connection, query, (player_name), fetch=True)

    def fetch_by_id(self, player_id:int):
        """
        Locate a given player or multiple players by id
        """

        query = "SELECT player_id, name, position, age FROM roster WHERE player_id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (player_id,))
            row = cursor.fetchone()

        if row:
            return Player(
                player_id= row[0],
                name=row[1],
                position=row[2],
                age=row[3],
                team=row[4]
            )
        
        return None 





class SessionRepository:
    def __init__(self, connection):
        #Initialize a SessionRepository object with a connection to an existing database
        self.connection = connection

    def add_session(self, session):
        query = """
        INSERT INTO sessions (player_id, session_date, duration_minutes, sprint_count, total_distance, max_speed, touches_left, touches_right)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(self.connection, query, 
                      (session.player.player_id, session.minutes_played,
                       session.distance_covered, session.sprints, session.defensive_actions))

    
    def get_sessions_by_player(self, player_id):
        """
        Queries sessions from a given player
        """
        query = "SELECT * FROM Sessions WHERE player_id = %s"
        return execute_query(self.connection, query, (player_id,), fetch=True)
    
    
    def delete_session(self, session_id):
        """
        Deletes a single session by session_id.
        """
        try:
            query = "DELETE FROM sessions WHERE session_id = %s"
            with self.connection.cursor() as cursor:
                execute_query(self.connection, query, (session_id))
                affected_rows = cursor.rowcount  # Number of rows affected
            self.connection.commit()
            logging.info(f"Session {session_id} successfully deleted.")
            return affected_rows > 0  # True if deletion succeeded, False if no record found
        
        except pymysql.MySQLError as e:
            logging.info(f"Error while deleting session. : {e}")
            self.connection.rollback()  # Ensures the database stays consistent if something fails
            
            return False  # Lets the application logic know whether the deletion actually occurred. 
        

    def delete_sessions_by_player(self, player_id):
        """
        Deletes all sessions linked to a specific player.
        
        Args:
            player_id (int): The player's unique ID.
        
        Returns:
            int: Number of sessions deleted.
        """
        try:
            query = "DELETE FROM Sessions WHERE player_id = %s"
            with self.conn.cursor() as cursor:
                cursor.execute(query, (player_id,))
                deleted_count = cursor.rowcount
            self.conn.commit()
            print(f"Deleted {deleted_count} sessions for player {player_id}.")
            return deleted_count

        except pymysql.MySQLError as e:
            print(f"Error while deleting sessions for player {player_id}: {e}")
            self.conn.rollback()
            return 0
