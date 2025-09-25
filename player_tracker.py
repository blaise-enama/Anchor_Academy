import mysql.connector
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
            import pymysql
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

        """if conn.is_connected():
            db_info = conn.get_server_info()
            logging.info(f"successfully connected to MySQL Server version {db_info}")
            cursor = conn.cursor()
            cursor.execute("SELECT Anchor_Academy();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record[0]}")"""
    
    except Error as e:
        logging.info(f"Error while connecting to MySQL: {e}")
        conn = None

    """finally:
        if 'connection' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")"""

    return conn


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
        # a method for determining the ratio of touches between left and right 
        total_touches = self.touches_left + self.touches_right
        return self.touches_right / total_touches if total_touches else 0

        
    def work_rate(self):
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
        
    

    