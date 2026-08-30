import logging
from os import name
from anchor_academy.src.models.player_tracker import *
from anchor_academy.src.models.session_metrics import SessionMetric
from anchor_academy.src.repositories.playerRepo import PlayerRepository
from anchor_academy.src.repositories.sessionRepo import SessionRepository
from fake_repos.fake_roster import FakePlayerRepo
from fake_repos.fake_sessions import FakeSessionRepo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class PlayerService:
    def __init__(self,playerRepo: PlayerRepository, sessionRepo: SessionRepository):
        self.player_repo = playerRepo
        self.session_repo = sessionRepo
        #self.fake_roster = fakeRoster
        #self.fake_sessions = fake_sessionRepo

    def add_player(self,name:str, age:int, position:str , team:str, player_id=None)->Player:
        """
        function to create and add a player object to the player repository

        returns a player object with the same parameters in the definition
        """
        print("Creating Player object...")
        print(Player)
        print(Player.__module__)

        #validate inputs
        if not name:
            raise ValueError("Player name is required. Try again")
        if age is None:
            raise ValueError("Player age is required. Try again")
        if age <= 10:
            raise ValueError("Player must be at least 10 years of age")
         
        

        #create a domain Player object
        player = Player(
            name= name,
            age=age,
            position= position,
            team= team

        )
                

        player = self.player_repo.add_player(player)
        logging.info(f"Player {player.name} added to database with ID {player.player_id}")

        return player       
    
    
    
    def get_player(self,player_name):
        "A function that retrieves a player object by calling the locat_player function from the Repo"
        row = self.player_repo.locate_player(player_name)

        if not row:
            return None
        

        return Player(
            player_id= row[0],
            name = row[1],
            age=row[2],
            position=row[3],
            team=row[4]
        )

    def list_players(self):
        """
        calls get_roster from the playerRepo and turns each row into a domain player object
        """
        rows = self.player_repo.get_roster()
        roster = []

        for r in rows:
            if isinstance(r, dict):
                pid = r.get("player_id")
                name = r.get("name")
                position = r.get("position")
                age = r.get("age")
                team = r.get("team")
            else:
                # fallback tuple ordering: (id, name, position, age, team)
                pid, name, position, age, team = r

            roster.append(
                Player(
                    player_id=pid,
                    name=name,
                    position=position,
                    age=age,
                    team=team,
                )
            )

        return roster

    
    

    def get_player_with_sessions(self, *, player_id=None, name=None):
        """
        A function that returns a player object as well as their corresponding sessions
        """
        
        #If neither player_id nor name provided, raise a valueError
        if not player_id and not name:
            raise ValueError("player_id or name must be provided")
        
        #If just player_id is provided, locate player by ID. Otherwise, locate them by name if provided
        if player_id is not None:
            #row = self.fake_roster.get_by_id(player_id)
            row= self.player_repo.fetch_by_id(player_id) 
            logging.info(f"Retrieved player by id: {row}")
            print(f"Roster lookup returned: {row}")
        else:
            row = self.player_repo.get_by_name(name)
            logging.info(f"Retrieved player by name: {row}")
            print(f"Roster lookup returned: {row}")
            #self.fake_roster.locate_player(name)

        #IF neither are provided, return none
        if not row:
            return None
        
        #create a Player object using data pulled from a database
        #maps each value from the database row into a named attribute
        #conceptually, this converts raw database data into a domain object
        player = Player(
            player_id=row["player_id"] if isinstance(row, dict) else row[0],
            name=row["name"] if isinstance(row, dict) else row[1],
            position=row["position"] if isinstance(row, dict) else row[2],
            age=row["age"] if isinstance(row, dict) else row[3],
            team=row["team"] if isinstance(row, dict) else row[4],
        )

        #use the get_player_sessions function and id attribute to retrieve the above player object's sessions
        #sessions = self.fake_sessions.list_sessions_by_player(player.player_id)
        sessions = self.session_repo.get_player_sessions(player.player_id)

        #iterate through the session objects, and store a list of sessions 
        player.sessions = []

        for s in sessions:

            session = Session(
                session_id=s["session_id"] if isinstance(s, dict) else s[0],
                player_id=s["player_id"] if isinstance(s, dict) else s[1],
                session_date=s["session_date"] if isinstance(s, dict) else s[2],
                sprint_count=s["sprint_count"] if isinstance(s, dict) else s[4],
                total_distance=s["total_distance"] if isinstance(s, dict) else s[5],
                max_speed=s["max_speed"] if isinstance(s, dict) else s[6],
                touches_left=s["touches_left"] if isinstance(s, dict) else s[7],
                touches_right=s["touches_right"] if isinstance(s, dict) else s[8],
                #dominant_foot=s["dominant_foot"] if isinstance(s, dict) else s[9],
            )

            # add metrics (SessionMetric constructor may differ; adapt if needed)
            session.add_metric(SessionMetric("total_distance", s["total_distance"] if isinstance(s, dict) else s[5], "m"))
            session.add_metric(SessionMetric("sprints", s["sprint_count"] if isinstance(s, dict) else s[4], "count"))
            session.add_metric(SessionMetric("max_speed", s["max_speed"] if isinstance(s, dict) else s[6], "km/h"))
            session.add_metric(SessionMetric("touches_left", s["touches_left"] if isinstance(s, dict) else s[7], "touches"))
            session.add_metric(SessionMetric("touches_right", s["touches_right"] if isinstance(s, dict) else s[8], "touches"))
            
            player.sessions.append(session)
        return player


    def delete_player(self, player_id):
        if player_id is None:
            raise ValueError("Player ID is required. Enter a valid ID to delete player from the database.")
        
        player = self.player_repo.fetch_by_id(player_id)

        if player is None:
            raise RuntimeError(
                f"Player with ID {player_id} does not exist."
            )
        self.player_repo.delete_player(player_id)