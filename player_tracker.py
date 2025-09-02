import mysql
import csv
from mysql.connector import Error
from datetime import datetime


def connect_to_database(host_name, user_name, user_password, database):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd= user_password,
            db= database
        )
        print("MySQL Database connection successful!") 
            
        #host= 'localhost',
        #user='root@localhost',             #Use to write a unit test for this function 
        #password='Enamfam.7',
        #database='Anchor_academy.roster'
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return connection


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
        this is a loader function that reads the file exported from the Playermaker tracker, and
        creates a Session object for each record, and savees it to the database. 

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

    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (player_id, date, duration, distance, sprint_count, max_speed, touches_left, touches_right) 
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
        
    

    