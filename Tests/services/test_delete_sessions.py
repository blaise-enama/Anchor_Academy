import pytest
from datetime import date
from anchor_academy.player_tracker import Session
from anchor_academy.services.session_services import SessionService
from tests.fakes.FakeSessionRepo import FakeSessionRepo

def test_delete_session_removes_session():
    sessions = [
        Session(1, 1, date.today(), 60, 5000, 20, 30, 40, 60),
        Session(2, 1, date.today(), 55, 4800, 18, 28, 50, 50),
    ]

    repo = FakeSessionRepo(sessions)
    service = SessionService(repo)

    result = service.delete_session(1)

    assert result is True
    assert len(repo.sessions) == 1
    assert repo.sessions[0].session_id ==2