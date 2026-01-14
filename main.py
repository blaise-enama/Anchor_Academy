from player_tracker import *
from datetime import datetime, date

def main():
    """
    this main function creates a player/ multiple players, and a training session for that player. 
    player ID is auto-fetched using cursor.lastrowid to ensure that the session is linked to the correct player
    """
    # Establish a connection with the current Anchor_Academy Database
    # connection = connect_to_database('localhost','root', 'Enamfam.7', 'Anchor_Academy') #Using mysql-connector-python

    conn = connect_to_database()
    if not conn:
        return

    #create repositories
    player_repo = PlayerRepository(conn)
    session_repo = SessionRepository(conn)

    player_repo.get_roster()
    
    conn.close()
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