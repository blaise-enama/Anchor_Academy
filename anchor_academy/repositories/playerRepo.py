from anchor_academy.player_tracker import *

class PlayerRepository:
    """
    This is a Repository class designed to store the player table
    """
    def __init__(self, conneciton):
        self.connection = conneciton

    def create_roster_table(self):
        """
        creates a table named roster, to store all player data/ objects
        should be created upon app installation. 
        """
        query = """
        CREATE TABLE roster(
        player_id,
        name,
        position,
        age, 
        team
        )
    
        """

    def add_player(self, player:Player)->Player:
        """
        adds a player object to the repository 
        runs SQL and stores data. 
        """
        query = """
        INSERT INTO roster (name, position, age, team)
        VALUES (%s,%s,%s,%s)
        """
        logging.info(f"query: {query}")
        logging.info(f"player id: {query.count("%s")}")

        with self.connection.cursor() as cursor:
            cursor.execute(query, (player.player_id,
                                   player.name,
                                   player.position,
                                   player.age,
                                   player.team))

            #player.player_id = cursor.lastrowid #captures generated ID

        #execute_query(self.connection, query, (player.name, player.position, player.age, player.team))
        self.connection.commit()
        return cursor.lastrowid


    def get_roster(self):
        """
        Displays the full roster from a mysql database.
        returns a roster consisting of a list of player objects opposed to dictionaries
        """

        query = "SELECT * FROM roster"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query )
            return cursor.fetchall()

        #return [Player(**row) for row in rows]
    

    def delete_player(self, player_name):
        query= "DELETE FROM roster WHERE name = %s"
        execute_query(self.connection, query)
        logging.info(f"Successfully deleted player {player_name} from the database")

    
    def locate_player(self,player_name):
        """Locates a given player by name 
        
        """
        query = "SELECT * FROM roster WHERE name = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (player_name,)) #The trailing comma is required to make player_name a 1-element tuple
            return cursor.fetchone() #fetchone ensures only one row is returned
            # return cursor.fetchall() ## fetchall if player names are NOT unique 


    def fetch_by_id(self, player_id:int):
        """
        Locate a given player or multiple players by id
        """

        query = "SELECT player_id, name, position, age FROM roster WHERE player_id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (player_id,))
            return cursor.fetchone()

         