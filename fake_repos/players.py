from anchor_academy.repositories import *
from anchor_academy.player_tracker import *


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
        return self.players.get(player_id)
    

    def get_by_name(self, name):
        for player in self.players.values():
            if player[1] == name:
                return player
        return None
    
