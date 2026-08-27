from anchor_academy.src.repositories import *
from anchor_academy.src.models.player_tracker import *


class FakePlayerRepo:

    def __init__(self):
        self.players = {
            1: (1, "Blaise Enama", "F",25, "Anchor Academy"),
            2: (2, "Regis Enama", "CB", 25, "Anchor Academy"),
            3: (3, "Joe Schmoe", "CM",27, "BW Gottschee"),
            4: (4, "Jane Doe", "CM",22, "Anchor Academy" ),
            5: (5, "John Doe","RB", 23, "Anchor Academy"),
            6: (6, "Nia Carter", "LW", 26, "Anchor Academy")
        }

    def get_by_id(self, player_id):
        for player in self.players.values():
            if player[0] == player_id:
                return player
        return None    

    def get_by_name(self, name):
        for player in self.players.values():
            if player[1] == name:
                return player
        return None
    
    def get_roster(self):
        return list(self.players.values())
    
    
    def add_player_to_fake_repo(self, player: Player):
        """
        adds a player object to the repository 
        runs SQL and stores data. 
        """
        new_id = max(self.players.keys()) + 1
        self.players[new_id] = (new_id, player.name, player.position, player.age, player.team)
        return new_id
    

    def save_to_fake_db(self, player: Player):
        """
        Simulates saving a player to the database.
        In a real implementation, this would involve executing an SQL INSERT statement.
        """
        new_id = self.add_player_to_fake_repo(player)
        return new_id
