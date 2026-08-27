import logging
import pandas as pd
from anchor_academy.src.models.session import Session
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from typing import List, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')




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
            self.player_id,
            self.name,
            self.position,
            self.age,
            self.team
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
            """, (self.player_id, s.session_date, s.distance, s.sprints, s.top_speed,
                  s.touches_left, s.touches_right, s.accels, s.decels, s.duration, s.fatigue))
        conn.commit()
        #player_id = cursor.lastrowid
        return cursor.lastrowid