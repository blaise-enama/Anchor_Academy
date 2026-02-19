import random
from datetime import date, timedelta



class FakeSessionRepo:
    def __init__(self, sessions=None):
        self.sessions: dict[int, list[tuple]] = {}
        self._seed_sessions()

    def _seed_sessions(self):
        """
        Instead of testing this application with a real database, we will simulate a sessions data repository,
        given five players, and 8-10 sessions each.

        This substitutes the need for a csv, which would hypothetically do the same thing as this function(return a dataset)
        """
        base_date = date(2026, 2, 9)

        for player_id in range(1, 6):  # 5 players
            self.sessions[player_id] = []  #creates an storage for each player_id key

            num_sessions = random.randint(8, 10)  # a random number of sessions between 8 to 10
            
            for i in range(num_sessions): # in that range of the random number...
                #create a session date
                session_date = base_date + timedelta(days=i * 7)

                # update the player's session with the following data:
                self.sessions[player_id].append(
                    (
                        1000 + player_id * 100 + i,   # session_id
                        player_id,                   # player_id
                        session_date,                # session_date
                        random.randint(70, 95),      # duration_minutes
                        random.randint(8500, 10500), # total_distance
                        random.randint(10, 25),      # sprint_count
                        round(random.uniform(25, 33), 1),  # max_speed
                        random.randint(20, 50),      # touches_left
                        random.randint(30, 70),      # touches_right
                    )
                )
        

    def get_all(self):
        return [
            session
            for player_sessions in self.sessions.values()
            for session in player_sessions
            ]
    

    def list_sessions_by_player(self, player_id):
        return self.sessions.get(player_id, [])
    
    
    def delete_session(self, session_id):
        for player_id, player_sessions in self.sessions.items():
            for i, session in enumerate(player_sessions):
                if session[0] == session_id:  # session_id is at index 0
                    del player_sessions[i]
                    return True
        return False
    