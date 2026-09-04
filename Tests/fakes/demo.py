import pytest 
from anchor_academy.src.models import player_tracker
from fake_repos.fake_roster import FakePlayerRepo
from fake_repos.fake_sessions import FakeSessionRepo


####### Fake roster tests #####
#Simulates the real repository

@pytest.fixture 
def player_repo():
    """Create a fresh FakePlayerRepo for each test."""
    return FakePlayerRepo()


def test_get_roster(player_repo):
    roster = player_repo.get_roster()

    assert len(roster) == 6

