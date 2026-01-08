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
    
    player_repo.add_player(player)


def display_players(player_repo):
    players = player_repo.get_roster()
    for p in players:
        print(p)

def delete_player(args, player_repo):
    player_repo.delete(args.player_id)


def main():
    parser = argparse.ArgumentParser(description= "Player Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    #------- Add Player -------
    add_player_parser = subparsers.add_parser("add-player")
    #add_player_parser.add_argument("--id", type=int, required=True)
    add_player_parser.add_argument("--name", type=str, required=True)
    add_player_parser.add_argument("--position", type=str, required=True)
    add_player_parser.add_argument("--age", type=int, required=True)
    add_player_parser.add_argument("--team", required=True)


    # ---- Delete Player ----
    delete_player_parser = subparsers.add_parser("delete-player")
    delete_player_parser.add_argument("--player-id", type=int, required=True)

    # ---- List Players ----
    subparsers.add_parser("list-players")
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
        delete_player(args, player_repo)
    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()

