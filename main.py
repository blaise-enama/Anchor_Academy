import mysql.connector
from player_tracker import *
from datetime import datetime, date

def main():
    #Connect to MySQL

    conn = mysql.connector.connect(
        host = "localhost",
        user = "root@locahost",
        password = "Enamfam.7",
        database = "Anchor_Academy"
    )

    # Create Player instance
    player = Player(3, "Lionel Messi", "F", 36, "Inter Miami")
    player_id = player.save_to_db()
    print(f"Player '{player.name}' saved with ID {player_id}")

 
    #add Sessions
    session = Session(player_id, date.today(), 120, 10.5,15, 24.7, 137, 52)
    #player.add_session(Session(datetime(2025, 8, 12), 120, 9.8, 18, 31.2, 38, 42))

    # Save players and Sessions
    session.save_to_db()
    print(f"Session successfully saved to database for Player ID {player_id}")


    if __name__ == "__main__":
        main()