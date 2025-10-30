from player_tracker import *

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
        
        query = "SELECT * FROM Sessions WHERE player_id = %s"
        return execute_query(self.connection, query, (player_id,), fetch=True)
    
    
    def delete_session(self, session_id):
        """Deletes a single session by session_id.
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

    

