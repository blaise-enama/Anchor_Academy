import mysql.connector
import pymysql
import csv
import logging
import pandas as pd
from mysql.connector import Error
from datetime import datetime
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def connect_to_database(host_name, user_name, user_password, database,driver="mysql-connector"):
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
            
        #host= 'localhost',
        #user='root@localhost',             #Use to write a unit test for this function 
        #password='Enamfam.7',
        #database='Anchor_academy'
    
    except Error as e:
        logging.info(f"Error while connecting to MySQL: {e}")
        conn = None

    return conn

def execute_query(conn,query, params=None):
    """
    Execute a query safely with pymysql
    do i need this function if I can just run cursor.execute("SELECT...;")
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params) 
            conn.commit()

    except Exception as e:
        logging.info(f"Error executing query: {e}")
    
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
    def __init__(self, player_id, name, position, age, team):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.age = age 
        self.team = team
        self.sessions = [] # stores multiple Sessions objects

    def add_session(self,session):
        self.sessions.append(session)


    def save_to_db(self,conn):
        cursor = conn.cursor() # establish a connection with the server
        cursor.execute("""
            INSERT INTO roster (player_id,name, position, age, team) 
            VALUES (%s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE name=%s, position=%s, age=%s
        """,(self.player_id, self.name, self.position, self.age, self.team)
        )
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
    def __init__(self, conneciton):
        self.connection = conneciton

    def add_player(self, player):
        query = """
        INSERT INTO roster (player_id, name, position,age, team)
        VALUES (%s,%s,%s,%s,%s)
        """
        execute_query(self.connection, query, (player.name, player.position, player.age, player.team))

    def get_all_players(self):
        query = "SELECT * FROM roster"
        return execute_query(self.connection, query, fetch=True)
    

class SessionRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_session(self, session):
        query = """
        INSERT INTO Sessions (player_id, session_date, duration_minutes, sprint_count, total_distance, max_speed, touches_left, touches_right)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(self.connection, query, 
                      (session.player.player_id, session.minutes_played,
                       session.distance_covered, session.sprints, session.defensive_actions))

    
    def get_sessions_for_player(self, player_id):
        query = "SELECT * FROM Sessions WHERE player_id = %s"
        return execute_query(self.connection, query, (player_id,), fetch=True)
    

    