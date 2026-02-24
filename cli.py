import argparse
import logging
from anchor_academy.player_tracker import *
from anchor_academy.repositories.sessionRepo import SessionRepository
from anchor_academy.repositories.playerRepo import PlayerRepository
from anchor_academy.services.session_services import SessionService
from anchor_academy.services.player_service import PlayerService
from fake_repos.players import FakePlayerRepo
from fake_repos.fake_sessions import FakeSessionRepo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

"""
CLI is used for triggering the system behavior upon [user] request. 
They should be used as a human entry point for data ingestion
functions defined here Should call a respective PlayerService method 
No object creation, no SQL logic, just handles user input"""

def add_player(args, player_service):
    #call the add_player method from the service layer
   player = player_service.add_player(
        name=args.name,
        position=args.position, 
        age=args.age, 
        team=args.team
    )
   print(f"player added successfully (id={player})")

def display_players(args, player_service):
    #trigger the service function to list players
    players = player_service.list_players()
    
    if not players:
        print("No players found.")
        return
    
    for player in players:
        print(
            f"ID: {player.player_id} | "
            f"Name: {player.name} | "
            f"Age: {player.age} | "
            f"Position: {player.position} | "
            f"Team: {player.team}"
        )
    

def delete_player(args, player_repo):
    player_service = PlayerService(player_repo)
    player_service.delete
    player_repo.delete_player(args.player_name)


def locate_player(args, player_service):
    try:
        player = player_service.get_player(args.name)

        if not player:
            print(f"No player found with name '{args.name}'")
            return
        
        print(
            f"\nPlayer ID: {player.player_id} |"
            f"Name: {player.name} |"
            f"Age: {player.age} |"
            f"Position: {player.position} |"
            f"Team: {player.team} |"
        )
    except Exception as e:
        print(f"Errors {e}")


def add_session(args, session_repo):
    session_service = SessionService(session_repo)

    session = Session(
        player_id=args.player_id,
        session_date=args.session_date,
        duration_minutes=args.duration_minutes,
        sprint_count=args.sprint_count,
        total_distance=args.total_distance,
        max_speed=args.max_speed,
        touches_left= args.left_touches,
        touches_right= args.right_touches
        
    )
    session_repo.add_session(session)

def handle_add_session(args):
    conn = connect_to_database()
    session_repo = SessionRepository(conn)
    session_service = SessionService(session_repo)

    session_id = session_service.add_Session(
        player_id= args.player_id,
        session_date=args.session_datel,
        duration_minutes= args.duration_minutes,
        sprint_count= args.sprint_count,
        total_distance= args.total_distance, 
        max_speed=args.max_speed,
        touches_left= args.touches_left,
        touches_right= args.touches_right)
    logging.info(f"Session {session_id} added successfully!")


def list_sessions(args, session_repo):
    """
    lists all the sessions recorded in the database
    """
    session_service = SessionService(session_repo)
    sessions = session_service.list_sessions()

    if not sessions:
        print("No sessions found.")
        return
    for s in sessions:
        print(
            f"Session ID: {s.session_id} | "
            f"Player ID: {s.player_id} | "
            f"Date: {s.session_date} | "
            f"Duration: {s.duration} min | "
            f"Sprints: {s.sprints} |"
            f"Distance: {s.distance} m | "
            f"Max Speed: {s.max_speed} | "
            f"Left Touches: {s.touches_left} |"
            f"Right Touches: {s.touches_right} |"
        )


def list_player_sessions(args, player_service):

    try:
        player = player_service.get_player_with_sessions(
            player_id=args.id,
            name= args.name )
        
        # if player DNE, print a message
        if not player:
            print(f"No matching player found. Enter a valid player name or ID")
            return
        #otherwise, print the name and ID, followed by age, position, and team
        print(
            f"\nPlayer: {player.name} (ID: {player.player_id})\n"
            f"Age: {player.age} | Position: {player.position} | Team: {player.team}\n"
            f"{'-' * 43}"
        )

        #if no sessions are recorded for the player selected, print message
        if not player.sessions:
            print(f"No sessions recorded")
            return
        
        for s in player.sessions:        
            print(
                f"Session ID: {s.session_id} | "
                f"Date: {s.session_date} | "
                f"Duration: {s.duration} min | "
                f"Sprints: {s.sprints} | " 
                f"Distance: {s.distance} m | "
                f"Max Speed: {s.max_speed} | "
                f"Left Touches: {s.touches_left} | "
                f"Right Touches: {s.touches_right} |"
            ) 

    except Exception as e:
        print(f"Error: {e}")
    
   # logging.info(f"Response type: {type(player.sessions)}")


def delete_session(args, session_service):
    try:
        session_service.delete_session(args.session_id)
        print(f"Session {args.session_id} deleted successfully")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description= "Player Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    #------- Add Player -------
    add_player_parser = subparsers.add_parser("add-player")
    add_player_parser.add_argument("--name", type=str, required=True)
    add_player_parser.add_argument("--position", type=str, required=True)
    add_player_parser.add_argument("--age", type=int, required=True)
    add_player_parser.add_argument("--team", required=True)


    # ---- locate player ----
    locate_player_parser= subparsers.add_parser("find-player", help="Find a player by name")
    locate_player_parser.add_argument("--name", type=str, required=True, help="Full name of the player")

    # ---- Delete Player ----
    delete_player_parser = subparsers.add_parser("delete-player")
    delete_player_parser.add_argument("--name", type=str, required=True)

    # ---- List Players ----
    subparsers.add_parser("list-players")

    # ---- Add Session ----
    add_session_parser = subparsers.add_parser("add-session", help="Add a training or match session for a player")
    add_session_parser.add_argument("--player_id", type=int, required=True)
    add_session_parser.add_argument("--session_date", required=True,
                                    help="Date of session (YYYY-MM-DD)")
    add_session_parser.add_argument("--duration_minutes", type=int, required=True)
    add_session_parser.add_argument("--sprint_count", type=int, required = True)
    add_session_parser.add_argument("--total_distance", type=float, required=True)
    add_session_parser.add_argument("--max_speed", type=float, default=0, required=True)
    add_session_parser.add_argument("--left_touches", type=int, default=0)
    add_session_parser.add_argument("--right_touches", type=int, default=0)
    add_session_parser.set_defaults(func=handle_add_session)


    # ---- Delete Sessions ----
    delete_session_parser = subparsers.add_parser("delete-session")
    delete_session_parser.add_argument("--session-id", type=int, required=True)


    # ---- Display Sessions ----
    subparsers.add_parser("list-sessions", help="Display all sessions recorded for every player")

    #---- Display sessions by player ID -----
    player_session_parser=subparsers.add_parser("player-sessions", help="Display all sessions recorded for a player, along with their details.")
    player_session_parser.add_argument("--id", type=int, required=False, help="Player ID")
    player_session_parser.add_argument("--name", type=str, required=False,help="Player name")


    args = parser.parse_args()
    
    conn = connect_to_database()
    if not conn:
        return
    
    player_repo = FakePlayerRepo()
    #PlayerRepository(conn)
    session_repo = FakeSessionRepo()
    #SessionRepository(conn)
    session_repo._seed_sessions()

    session_service = SessionService(session_repo)
    player_service = PlayerService(player_repo, session_repo)

    if args.command == "add-player":
        add_player(args, player_repo)
    if args.command == "find-player":
        locate_player(args, player_service)
    elif args.command == "list-players":
        display_players(args,player_service)
    elif args.command == "delete-player":
        #automatically deletes a player as well as their sessions via cascade
        delete_player(args, player_repo)
    elif args.command == "add-session":
        add_session(args, session_repo)
    elif args.command == "list-sessions":
        list_sessions(args, session_repo)
    elif args.command == "delete-session":
        delete_session(args, session_service)
    elif args.command == "player-sessions":
        list_player_sessions(args, player_service)

    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()

