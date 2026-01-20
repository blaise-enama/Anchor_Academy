import logging
from datetime import datetime
from player_tracker import Session
from player_tracker import SessionRepository


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class SessionService:
    def __init__(self, sessionRepo: SessionRepository):
        self.sessionRepo = sessionRepo
        
    def add_Session(self, player_id,session_date, duration_minutes, sprint_count, total_distance, max_speed, touches_left, touches_right):
        session_date = datetime.strptime(
        session_date, "%Y-%m-%d").date()

        #create a domain object
        session = Session(
        player_id=player_id,
        session_date=session_date,
        duration_minutes=duration_minutes,
        sprint_count=sprint_count,
        total_distance = total_distance,
        max_speed= max_speed,
        touches_left= touches_left,
        touches_right= touches_right
        )


        
        logging.info(f"session added to database for player {player_id}")
        return self.sessionRepo.add_session(session)