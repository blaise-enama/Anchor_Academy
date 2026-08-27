import pytest
from datetime import date
from anchor_academy import *
from anchor_academy.player_tracker import Session
from anchor_academy.src.services.session_services import SessionService
from tests.fakes.session_repo import FakeSessionRepo

def test_get_all_sessions_returns_all_sessions():
    #create session objects
    sessions = [
        Session(1, 1, date.today(), 60, 5000, 20, 30, 40, 60),
        Session(2, 2, date.today(), 55, 4800, 18, 28, 50, 50),
        Session(2, 1, date.today(), 70, 6200, 25, 32, 45, 55),
    ]

    repo = FakeSessionRepo(sessions)
    service = SessionService(repo)

    result = service.list_sessions()

    assert len(result) == 44
    assert result == sessions


