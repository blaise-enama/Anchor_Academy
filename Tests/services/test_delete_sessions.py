import pytest
from datetime import date
from anchor_academy.player_tracker import Session
from anchor_academy.services.session_services import SessionService
from tests.fakes.session_repo import FakeSessionRepo

def test_delete_session_removes_session():

    repo = FakeSessionRepo(
        sessions= {
            1: [
                (1, 1, date.today(), 60, 20, 5000, 30, 40, 60),
                (2, 1, date.today(), 55, 18, 4800, 28, 50, 50),
            ]    
        }   
    )
    service = SessionService(repo)
    result = service.delete_session(1)

    assert result is True
    assert len(service.list_sessions()) == 1  
    
    service = SessionService(repo)



def test_delete_nonexistent_session_raises_error():
    repo = FakeSessionRepo(
        sessions= {
            1: [
                (1, 1, date.today(), 60, 20, 5000, 30, 40, 60),
                (2, 1, date.today(), 55, 18, 4800, 28, 50, 50),
            ]    
        }   
    )
    service = SessionService(repo)
    result = service.delete_session(1)

    assert result is True
    assert len(service.list_sessions()) == 1

    with pytest.raises(RuntimeError):
        service.delete_session(999)
    

