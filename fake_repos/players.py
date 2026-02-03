from anchor_academy.repositories import *
from anchor_academy.player_tracker import *


class FakePlayerRepo:

    def __init__(self):
        self.players = {
            1: (1, "Blaise Enama", 25, "F", "Anchor Academy"),
            2: (2, "Regis Enama", 25, "CB", "Anchor Academy"),
            3: (3, "Joe Schmoe", 27, "CM", "BW Gottschee"),
            4: (4, "Jane Doe",22, "CM", "Gotham FC" )
        }

    def get_by_id(self, player_id):
        return self.players.get(player_id)
    

    def get_by_name(self, name):
        for player in self.players.values():
            if player[1] == name:
                return player
        return None
    
