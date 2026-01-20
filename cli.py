import argparse
import logging
from player_tracker import connect_to_database
from player_tracker import Player, Session, PlayerRepository, SessionRepository
from services.session_services import SessionService


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def add_player(args, player_repo):
    player = Player(
        name=args.name,
        position=args.position, 
        age=args.age, 
        team=args.team
    )
    
    saved_player = player_repo.add_player(player)
    print(f"Player created with ID {saved_player.player_id}")


def display_players(player_repo):
    players = player_repo.get_roster()
    for p in players:
        print(p)

def delete_player(args, player_repo):
    player_repo.delete_player(args.player_name)


def add_session(args, session_repo):
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



def delete_session(args, session_repo):
    session_repo.delete_session(args.session_id)


def main():
    parser = argparse.ArgumentParser(description= "Player Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    #------- Add Player -------
    add_player_parser = subparsers.add_parser("add-player")
    add_player_parser.add_argument("--name", type=str, required=True)
    add_player_parser.add_argument("--position", type=str, required=True)
    add_player_parser.add_argument("--age", type=int, required=True)
    add_player_parser.add_argument("--team", required=True)


    # ---- Delete Player ----
    delete_player_parser = subparsers.add_parser("delete-player")
    delete_player_parser.add_argument("--player-name", type=str, required=True)

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



    args = parser.parse_args()
    
    conn = connect_to_database()
    if not conn:
        return
    
    player_repo = PlayerRepository(conn)
    session_repo = SessionRepository(conn)

    if args.command == "add-player":
        add_player(args, player_repo)

    elif args.command == "list-players":
        display_players(player_repo)
    elif args.command == "delete-player":
        #automatically deletes a player as well as their sessions via cascade
        delete_player(args, player_repo)
    elif args.command == "add-session":
        session_service = SessionService(session_repo)
        session_service.add_session(
        player_id=args.player_id,
        session_date=args.session_date,
        duration_minutes=args.duration_minutes,
        sprint_count=args.sprint_count,
        total_distance=args.total_distance,
        max_speed=args.max_speed,
        touches_left=args.left_touches,
        touches_right=args.right_touches
        )


    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()

