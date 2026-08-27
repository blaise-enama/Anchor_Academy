from anchor_academy.src.models.player_tracker import *
"""
The services layer decides what SHOULD happen.
It services the CLI and "talks" to the database
Manipulates the data requested from the CLI (User) to be stored 
"""
class SessionRepository:
    def __init__(self, connection):
        #Initialize a SessionRepository object with a connection to an existing database
        self.connection = connection


    def create_sessions_table(self):
        query = """
                CREATE TABLE sessions(
                session_id,
                player_id,
                session_date,
                duration_minutes,
                sprint_count,
                total_distance,
                max_speed,
                touches_left,
                touches_right)
                """
        return execute_query(self.connection, query)


    def add_session(self, session):
        query = """
        INSERT INTO sessions (player_id, session_date, duration_minutes, sprint_count, total_distance, max_speed, touches_left, touches_right)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(self.connection, query, 
                      (session.player_id, session.session_date,
                       session.duration, session.sprints, 
                       session.distance, 
                       session.max_speed, session.touches_left, session.touches_right))
        

    
    def get_player_sessions(self, player_id=None, name=None):
        """
        Queries sessions from a given player
        """
        logging.info(f"Repo received player_id: {player_id} and name: {name} from the service")
        if player_id is None and name is None:
            raise ValueError("Either player_id or name must be provided")

        if player_id is None:
            query = """
            SELECT * 
            FROM sessions 
            WHERE player_id = (
                SELECT player_id 
                FROM roster 
                WHERE name = %s
            )
            ORDER BY session_date DESC
            """
            return execute_query(self.connection, query, (name,), fetch=True)
        
        query = """
        SELECT 
            session_id,
            player_id,
            session_date,
            duration_minutes,
            sprint_count,
            total_distance,
            max_speed,
            touches_left,
            touches_right
        FROM sessions 
        WHERE player_id = %s 
        ORDER BY session_date DESC
        """
        
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

    
    def get_all(self):
        """
        A query to retrieve all sessions data
        """
        query = """
            SELECT
                session_id,
                player_id,
                session_date,
                duration_minutes,
                sprint_count,
                total_distance,
                max_speed,
                touches_left,
                touches_right
                
            FROM sessions
            """
        
        cursor= self.connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()

        sessions = [
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
            for row in rows
        ]

        return sessions
    
        