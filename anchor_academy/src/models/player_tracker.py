import os
import mysql.connector
import pymysql.cursors
import csv
import logging
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


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
        # Use a dictionary cursor for better readability
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                logging.info("SELECT query executed")
                return cursor.fetchall()
            else:
                conn.commit()
                logging.info("query successfully executed")
                return cursor.lastrowid

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
        db_connection_str ='mysql+pymysql://root:Enamfam.7@localhost/Anchor_academy'
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
    def __init__(self,
                 player_id: Optional[int] = None,
                 name: str = '',
                 age: int = 0, 
                 position: str = '',
                 team: str = ''
        ):
        self.player_id = player_id
        self.name = name
        self.age = age 
        self.position = position
        self.team = team

        self.sessions: List[Session] = [] # stores multiple Sessions objects

    def __repr__(self):
        return (
            f"Player(player_id:{self.player_id}, Name: {self.name}, Age: {self.age}, Position: {self.position}, Team: {self.team})"
        )


    def add_session(self, session: "Session"):
        self.sessions.append(session)


    def save_to_db(self,conn):
        cursor = conn.cursor() # establish a connection with the server
        cursor.execute("""
            INSERT INTO roster (name, position, age, team) 
            VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE name=%s, position=%s, age=%s
        """,(self.name, self.position, self.age, self.team)
        )

        #save session data
        for s in self.sessions:
            cursor.execute("""
                INSERT INTO sessions (player_id, session_date, total_distance, sprint_count, top_speed,
                                       touches_left, touches_right, acceleration_events, deceleration_events,
                                       session_duration, fatigue_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.player_id, s.session_date, s.total_distance, s.sprint_count, s.max_speed,
                  s.touches_left, s.touches_right, s.accels, s.decels, s.duration, s.fatigue))
        conn.commit()
        #player_id = cursor.lastrowid
        return cursor.lastrowid







class Session:
    """
    Represents a single player session (e.g., training or match) within the system.

    This class models the core metadata of a session, including the player,
    session type, date, and duration. It is designed to work with a flexible
    metrics architecture, where all performance data (e.g., distance, sprints,
    speed) is stored separately as SessionMetric objects rather than as direct
    attributes of the Session.

    Attributes:
        session_id (Optional[int]): Internal unique identifier for the session (primary key in database).

        external_session_id (Optional[str]):   Identifier from an external system (e.g., Playermaker API) used for
            deduplication and data synchronization.

        player_id (Optional[int]): Foreign key linking the session to a specific player.

        session_type (Optional[str]):
            Type of session (e.g., "training", "match").

        session_date (Optional[datetime]):
            Date (and optionally time) when the session occurred.

        duration_minutes (Optional[int]):
            Total duration of the session in minutes.

        sessions (List[Session]):
            In-memory list intended for grouping or managing multiple session
            objects. (Note: this is not typically required for a single Session
            instance and may be better handled at the Player level.)

    Design Notes:
        - This class intentionally excludes performance metrics as attributes.
          Instead, metrics are stored in a separate SessionMetric model to allow
          for dynamic, extensible data ingestion (e.g., from Playermaker or other
          wearable devices).

        - This design supports scalable analytics and machine learning workflows,
          where new metrics can be added without modifying the Session schema.

    Example:
        session = Session(
            player_id=1,
            session_type="training",
            session_date=datetime(2026, 2, 20),
            duration_minutes=90
        )
    """
    def __init__(self, 
                 session_id: Optional[int] = None,
                 player_id: Optional[int] = None,
                 session_type: Optional[str] = None,
                 session_date: Optional[datetime] = None, 
                 duration_minutes: Optional[int] = None,
                 sprint_count: Optional[int] = None,
                total_distance: Optional[float] = None,
                max_speed: Optional[float] = None,
                touches_left: Optional[int] = None,
                touches_right: Optional[int] = None,
                dominant_foot: Optional[str] = None,
     ):
        self.session_id= session_id
        self.player_id = player_id
        self.session_type = session_type
        self.session_date = session_date
        self.duration_minutes = duration_minutes
        self.sprint_count = sprint_count
        self.total_distance = total_distance
        self.max_speed = max_speed
        self.touches_left = touches_left
        self.touches_right = touches_right
        self.dominant_foot = dominant_foot
        
        
        #initialize a list of sessions to be created to store multiple Session objects
        # think: Session.metrics = [Session(player_id=10,session_type='training', session_date=datetime(2026, 3, 22), duration=90)]
        self.metrics = []

    def add_metric(self, metric):
        """
        adds (appends) a new metric to the sessions list created in __init__
        """
        self.metrics.append(metric)

    def get_metrics_dict(self):
        """
        returns the session metrics as a dictionary 

        for every metric being recorded, map the metric name to a value 
        """
        return {m.metric_name: m.metric_value for m in self.metrics}
    
    def foot_usage_ratio(self):
        """
        determnines the ratio of touches between left and right 
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
            (self.player_id, self.session_date, self.duration_minutes, self.total_distance, self.sprint_count, self.max_speed, self.touches_left, self.touches_right)
        )

        conn.commit() #Commits current transaction.This method sends a COMMIT statement to the MySQL server, committing the current transaction.        conn.close()






