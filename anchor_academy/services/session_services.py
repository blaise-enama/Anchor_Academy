import logging
from datetime import datetime
from anchor_academy.player_tracker import Session
from anchor_academy.repositories.sessionRepo import SessionRepository


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


"""
Session service is designed to:
*parse the session date
*Create a Session object
*Compute work rate and other metrics
* Call the Session Respository
"""
class SessionService:
    def __init__(self, sessionRepo: SessionRepository):
        self.sessionRepo = sessionRepo
        
    def create_table(self, sessionRepo: SessionRepository):
        return self.sessionRepo.create_sessions_table()
    
    def add_session(self, player_id,session_date, duration_minutes, sprint_count, total_distance, max_speed, touches_left, touches_right):
        session_date = datetime.strptime(session_date, "%Y-%m-%d").date()

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

        session.dominant_foot= self.dominant_ft(session)
        
        logging.info(f"session added to database for player {player_id}")
        return self.sessionRepo.add_session(session)
    
    def list_sessions(self):
        return self.sessionRepo.get_all()
    
    def list_player_sessions(self, player_id):
        if player_id is None or player_id == 0:
            raise ValueError("Invalid Player ID. Please enter a valid player ID")
                
        rows = self.sessionRepo.get_player_sessions(player_id)
        sessions = []
        for row in rows:
            sessions.append(
                Session(
                session_id=row[0],
                player_id=row[1],
                session_date=row[2],
                duration_minutes=row[3],
                sprint_count=row[4],
                total_distance=row[5],
                max_speed=row[6],
                touches_left=row[7],
                touches_right=row[8]
            )
            )

        return sessions
    

    def delete_session(self, session_id):
        """Deletes a session, provided an existing session ID"""
        success = self.sessionRepo.delete_session(session_id)
        if not success:
            raise RuntimeError(f"Session {session_id} not found")
        return True
    

    def get_sessions(self):
        return self.sessionRepo.get_sessions_by_player()


    def compute_workrate(self, session):
        """
        A function for computing the workrate for a given session. 
        It uses fields such as the total duration, distance, and a sprint factor

        A basic work rate formula would be:
                Work Rate = Total Work Done / Time taken

        args:
        session: list (or session object?) 

        returns:
        a score to be stored in the sessions database
        This score is contingent on getting all the player's sessions, and calculating the combined sorkrate


                
        """
        if self.duration_minutes <= 0:
            return 0.0
        
        distance_per_min = session.total_distance / session.duration_minutes
        sprint_factor = session.sprint_count *10

        work_rate = distance_per_min + sprint_factor

        #round the work rate to the nearest third decimal point
        return round(work_rate, 2)
    

    def foot_usage_ratio(self, session):
        """
        a method for determining the ratio of touches between left and right 
        Returns right-foot usage ratio

        Range:
        0.0 = all left foot
        0.5 = balanced
        1.0  = all right foot
        """

        left_foot = session.touches_left
        right_foot = session.touches_right

        total_touches = left_foot + right_foot

        if total_touches == 0:
            return None 
        
        return round(right_foot / total_touches, 3)

    def dominant_ft(self, session):
        ratio = self.foot_usage_ratio(session)

        if ratio is None:
            return "unknown"
        elif ratio >0.5:
            return "right"
        elif ratio < 0.5:
            return "left"
        else:
            return "balanced"
