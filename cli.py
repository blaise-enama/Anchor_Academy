import argparse
import logging
from anchor_academy.src.models.player_tracker import *
from anchor_academy.src.repositories.sessionRepo import SessionRepository
from anchor_academy.src.repositories.playerRepo import PlayerRepository
from anchor_academy.src.services.session_services import SessionService
from anchor_academy.src.services.player_service import PlayerService
from fake_repos.fake_roster import FakePlayerRepo
from fake_repos.fake_sessions import FakeSessionRepo
from anchor_academy.database.setup import connect_to_database, initialize_anchor_academy    

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

"""
CLI is used for triggering the system behavior upon [user] request. 
They should be used as a human entry point for data ingestion
functions defined here Should call a respective PlayerService method 
No object creation, no SQL logic, just handles user input"""

    


def add_player(args, player_service):
    #call the add_player method from the service layer

    print("Adding a new player to the roster...")
    logging.debug(f"Received arguments: name={args.name}, age={args.age}, position={args.position}, team={args.team}")

    try:
        name= args.name
        age = args.age
        position = args.position
        team = args.team

        if not name:
            name = input("Player Name: ").strip()

        if age is None:
            age = int(input("Player Age: "))

        if not position:
            position = input("Player Position: ").strip()

        if not team:
            team = input("Player Team: ").strip()

        # Call the player service to add the player
        player = player_service.add_player(
            name=name,
            position=position, 
            age=age, 
            team=team
        )
        logging.info(f"Player {player.name} added successfully with ID {player.player_id}!")
        print(f"Player ID: {player.player_id} | Name: {player.name} | Age: {player.age} | Position: {player.position} | Team: {player.team} added successfully!")

    except Exception as e:
        logging.error(f"Error adding player: {e}")
        print(f"Error adding player: {e}")


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
    logging.info(f"Displayed {len(players)} players from the roster.")
    logging.info(f"Response type: {type(players)}")
    

def delete_player(args, player_service):
    try:
        player_id = args.player_id

        if player_id is None:
            player_id = int(input("Player ID: "))

        player_service.delete_player(player_id)
        logging.info(f"Player {player_id} has been successfully deleted.")
    
    except Exception as e:
        print(f"Error deleting player: {e}")


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
            f"Duration: {s.duration_minutes} min | "
            f"Sprints: {s.sprint_count} |"
            f"Distance: {s.total_distance} m | "
            f"Max Speed: {s.max_speed} | "
            f"Left Touches: {s.touches_left} |"
            f"Right Touches: {s.touches_right} |"
        )


def build_session_report(session):
        return {
        "session_id": session.session_id,
        "date": session.session_date,
        "duration": session.duration_minutes if hasattr(session, 'duration_minutes') else None,
        "distance": session.total_distance,
        "sprints": session.sprint_count if hasattr(session, 'sprint_count') else None,
        "max_speed": session.max_speed if hasattr(session, 'max_speed') else None,
        "touches_left": session.touches_left if hasattr(session, 'touches_left') else None,
        "touches_right": session.touches_right if hasattr(session, 'touches_right') else None,
        # "dominant_foot": session.dominant_foot if hasattr(session, 'dominant_foot') else None
    }


def list_player_sessions(args, player_service):

    try:
        player = player_service.get_player_with_sessions(
            player_id=args.player_id,
            name= args.name )
        print(player)
        
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
            report = build_session_report(s)
            print(
                f"Session ID: {report['session_id']} | "
                f"Date: {report['date']} | "
                f"Duration: {report['duration']} min | "
                f"Sprints: {report['sprints']} | "
                f"Distance: {report['distance']} m | "
                f"Max Speed: {report['max_speed']} km/h | "
                f"Touches Left: {report['touches_left']} | "
                f"Touches Right: {report['touches_right']} | "
                #f"Dominant Foot: {report['dominant_foot']} | "
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
    add_player_parser = subparsers.add_parser("add-player", help="Add a player to the roster")
    add_player_parser.add_argument("--name")
    add_player_parser.add_argument("--position")
    add_player_parser.add_argument("--age", type=int)
    add_player_parser.add_argument("--team")

    #------ Setup Database ------
    subparsers.add_parser("setup", help="Setup the Anchor Academy database")

    # ---- locate player ----
    locate_player_parser= subparsers.add_parser("find-player", help="Find a player by name")
    locate_player_parser.add_argument("--name", type=str, required=True, help="Full name of the player")

    # ---- Delete Player ----
    delete_player_parser = subparsers.add_parser("delete-player", help= "Delete a player from the roster")
    delete_player_parser.add_argument("--id", dest="player_id", type=str, required=False, help= "Player ID")

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
    player_session_parser= subparsers.add_parser("player-sessions", help="Display all sessions recorded for a player, along with their details.")
    player_session_parser.add_argument("--id", dest="player_id", type=int, required=False, help="Player ID")
    player_session_parser.add_argument("--name", type=str, required=False,help="Player name")

    
    print("Welcome to the Anchor Academy Player Tracker!")
    print("Your one stop tool for managing player profiles and tracking their training progress.")
    print("We track player development by recording their training sessions and analyzing their performance metrics.")

    print("Use this tool to improve your players' performance and help them reach their full potential through data-driven insights and analytics.")

    print("------------------------------------------------------------------------------------------------------------------------------------ \n")

    input("Before starting, please ensure that you have MySQL installed and running. Press any key to continue...")
    input("\nLet's get started! Press the Enter key to continue")
    
    use_real_db = input("Do you want to connect to a real database? (yes/no) [no]: ").strip().lower() =="yes"
    conn = None

    if use_real_db:
        # Try to create DB schema if needed and then connect interactively (prompts for credentials)
        logging.info(f"Default Databse setup")
        initialized = initialize_anchor_academy()  # uses env variabless if provided

        if not initialized:
            print("Database initialization failed or could not be completed.")
            choice = input("Continue in demo mode with in-memory data? (yes/no) [yes]: ").strip().lower() or "yes"
            if choice != "yes":
                print("Exiting. Goodbye!")
                return
            
        # Assuming initialization passed, Try interactive connection (prompts for host/port/user/pass if required)
        logging.info(f"real DB interactive mode triggered.")
        conn = connect_to_database(interactive=False)
        if not conn:
            print("Could not connect to the database. Falling back to demo mode with fake repositories.")
    
    else:
        #User entered "[no] to use_real_db"
        print("Running in demo mode with in-memory fake repositories.")

    if conn:
        player_repo = PlayerRepository(conn)
        session_repo = SessionRepository(conn)

    else:
        #there's no connection to a database(demo)
        player_repo = FakePlayerRepo()
        session_repo = FakeSessionRepo()
        session_repo._seed_sessions() #keep the demo data for interactive use


    session_service = SessionService(session_repo)
    player_service = PlayerService(player_repo, session_repo)

    while True:
        #initialize_anchor_academy() # Initialize the Anchor Academy database and connect to it
        command = input("Anchor Academy >").strip()
        if command == "" or command == "exit":
            print("Exiting Anchor Academy CLI. Goodbye!")
            break

        command_args = command.split()
        
        # Parse the command line arguments
        args = parser.parse_args(command_args)

        try:
            """if args.command == "setup":
                initialize_anchor_academy()"""
            if args.command == "add-player":
                logging.debug(f"Calling add_player with arguments: name={args.name}, age={args.age}, position={args.position}, team={args.team}")
                add_player(args, player_service)
                """save_player = input("Player added successfully! Would you like to save the player to the database? (yes/no): ").strip().lower()
                if save_player == "yes":

                    player_id = args.player_id,
                    name=args.name,
                    position=args.position, 
                    age=args.age, 
                    team=args.team"""
                
                logging.info(f"Player {args.name} saved successfully with ID {args.player_id}!")
                print(f"Player ID: {args.player_id} | Name: {args.name} | Age: {args.age} | Position: {args.position} | Team: {args.team} saved successfully!")


            elif args.command == "find-player":
                locate_player(args, player_service)

            elif args.command == "list-players":
                display_players(args,player_service)

            elif args.command == "delete-player":
                #automatically deletes a player as well as their sessions via cascade
                delete_player(args, player_service)

            elif args.command == "add-session":
                add_session(args, session_repo)

            elif args.command == "list-sessions":
                list_sessions(args, session_repo)

            elif args.command == "delete-session":
                delete_session(args, session_service)

            elif args.command == "player-sessions":
                print(args)
                print(f"Fetching sessions for player ID: {args.player_id} and name: {args.name}")
                list_player_sessions(args, player_service)
                #sessions = session_service.list_player_sessions(player_id=args.player_id, name=args.name)  
            elif args.command == "help":
                parser.print_help()

            else:
                break

        except Exception as e:
            logging.error(f"Error executing command '{args.command}'")
            print(f"Error: {e}")

    #conn.close()

if __name__ == "__main__":
    main()

