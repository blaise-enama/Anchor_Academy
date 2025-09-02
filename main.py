import mysql.connector
from player_tracker import *
from datetime import datetime, date

def main():
    """
    this main function creates a player/ multiple players, and a training session for that player. 
    player ID is auto-fetched using cursor.lastrowid to ensure that the session is linked to the correct player
    """
    #Connect to MySQL

    conn = connect_to_database('localhost','root', 'Enamfam.7', 'Anchor_Academy')

    # Create Player instance
    player = Player(3, "Lionel Messi", "F", 36, "Inter Miami")
    player_id = player.save_to_db(conn)
    print(f"Player '{player.name}' saved with ID {player_id}")

 
    #add Sessions
    session = Session(player_id, date.today(), 120, 45.7,15, 24.7, 137, 52)
    #player.add_session(Session(datetime(2025, 8, 12), 120, 9.8, 18, 31.2, 38, 42))

    # Save players and Sessions
    session.save_to_db()
    print(f"Session successfully saved to database for Player ID {player_id}")


    if __name__ == "__main__":
        main()