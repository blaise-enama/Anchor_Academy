import argparse
from player_tracker import connect_to_database
from player_tracker import Player, Session, PlayerRepository, SessionRepository

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
        sprints=args.sprint_count,
        distance_km=args.total_distance,
        max_speed=args.max_speed,
        touches_left= args.touches_left,
        touches_right= args.touches_right
        
    )
    session_repo.add(session)


def delete_session(args, session_repo):
    session_repo.delete_session(args.session_id)


def main():
    parser = argparse.ArgumentParser(description= "Player Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

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
    args = parser.parse_args()

    # ---- Add Session ----
    add_session_parser = subparsers.add_parser("add-session")
    add_session_parser.add_argument("--player-id", type=int, required=True)
    add_session_parser.add_argument("--date", required=True)
    add_session_parser.add_argument("--duration", type=int, required=True)
    add_session_parser.add_argument("--sprints", type=int, required = True)
    add_session_parser.add_argument("--distance", type=float, required=True)
    add_session_parser.add_argument("--max-speed", type=float, default=0, required=True)
    add_session_parser.add_argument("--left-touches", type=int, default=0)
    add_session_parser.add_argument("--right-touches", type=int, default=0)





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
        add_session(args, session_repo)
    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()

