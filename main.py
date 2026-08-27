from anchor_academy.src.models.player_tracker import *
from anchor_academy.database.setup import connect_to_database, initialize_anchor_academy
from anchor_academy.src.repositories.playerRepo import PlayerRepository
from fake_repos.fake_sessions import FakeSessionRepo
from fake_repos.players import FakePlayerRepo
from cli import *


from datetime import datetime, date

def main():
    """
    Tests the database connection, and the functionality of the Player and Session classes.
    """
    # Establish a connection with the current Anchor_Academy Database
    # connection = connect_to_database('localhost','root', 'Enamfam.7', 'Anchor_Academy') #Using mysql-connector-python

    initialize_anchor_academy()  # Initialize the Anchor Academy database and connect to it

    conn = connect_to_database()
    if conn:

        print("Successfully connected to the Anchor_Academy database.")
        print("Anchor Academy is now ready for use. You can now proceed to add players and sessions.")

        try:
                with conn.cursor() as cursor:

                    # Simple test query
                    cursor.execute("SELECT DATABASE();")

                    result = cursor.fetchone()

                    cursor.execute("SELECT * FROM roster;")
                    #roster = cursor.fetchall()

                    print(f"\nConnected Database: {result['DATABASE()']}")
                    #print(f"Roster Data: {roster}")

        except Exception as e:
            logging.info(f"Error running test query: {e}")

        finally:
            conn.close()
            logging.info(f"Database connection closed")

    else:
        logging.info(f"Failed to connect to database")

    
    #instantiate the player and session repositories
    #player_repo = PlayerRepository(conn)

    player_repo = FakePlayerRepo()
    session_repo =FakeSessionRepo()

    #Generate the fake sessions data 
    session_repo._seed_sessions()

    #prompt user to transition to the CLI for further interaction with the application
    print("\nWe will now transition you to the CLI for further interaction with the application.")  
    
    run_main()  # Call the run_main function to start the CLI  
    




"""

    # Create Player instance
    player = Player(3, "Lionel Messi", "F", 36, "Inter Miami")
    player_id = player.save_to_db(connection)
    print(f"Player '{player.name}' saved with ID {player_id}")

 
    #add Sessions
    session = Session(player_id, date.today(), 120, 45.7,15, 24.7, 137, 52)
    #player.add_session(Session(datetime(2025, 8, 12), 120, 9.8, 18, 31.2, 38, 42))

    # Save players and Sessions
    session.save_to_db(connection)
    print(f"Session successfully saved to database for Player ID {player_id}")

"""
if __name__ == "__main__":
    main()