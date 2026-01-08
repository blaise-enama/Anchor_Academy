from player_tracker import *


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
        INSERT INTO roster (player_id, name, position,age, team)
        VALUES (%s,%s,%s,%s,%s)
        """
        execute_query(self.connection, query, (player.name, player.position, player.age, player.team))


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
