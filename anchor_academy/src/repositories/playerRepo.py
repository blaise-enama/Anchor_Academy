from anchor_academy.src.models.player_tracker import *

class PlayerRepository:
    """
    This is a Repository class designed to store the player table
    """
    def __init__(self, connection):
        self.connection = connection

    def create_roster_table(self):
        """
        creates a table named roster, to store all player data/ objects
        should be created upon app installation. 
        """
        query = """
        CREATE TABLE roster(
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        position VARCHAR(255),
        age INT,
        team VARCHAR(255)
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
        

        with self.connection.cursor() as cursor:
            cursor.execute(
                query, 
                (
                    player.name,
                    player.position,
                    player.age,
                    player.team
                    )
                )
            self.connection.commit()

            player.player_id = cursor.lastrowid  # captures generated ID

        

        return player  # Return the player object with the assigned ID


    def get_roster(self):
        """
        Displays the full roster from a mysql database.
        returns a roster consisting of a list of player objects opposed to dictionaries
        """

        query = "SELECT * FROM roster;"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query )
            rows = cursor.fetchall()

        return rows

    

        #return [Player(**row) for row in rows]
    

    def delete_player(self, player_id):

        query= "DELETE FROM roster WHERE player_id = %s"
        execute_query(self.connection, query, (player_id,))

    
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

        query = "SELECT * FROM roster WHERE player_id = %s"

        rows = execute_query(self.connection, query, (player_id,), fetch = True)
        if not rows:
            return None
        
        return rows[0]
    

         