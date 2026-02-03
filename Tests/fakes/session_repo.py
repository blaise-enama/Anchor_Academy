from fake_repos.sessions import FakeSessionRepo

def __init__(self, sessions=None):
    self.sessions = sessions or []

def get_all_sessions(self):
    return self.sessions

def add_session(self, session):
        self.sessions.append(session)
        return session


def list_sessions_by_player(self, player_id):
        return [
            session for session in self.sessions
            if session.player_id == player_id
        ]


def delete_session(self, session_id):
        initial_len = len(self.sessions)
        self.sessions = [
            s for s in self.sessions if s.session_id != session_id
        ]
        return len(self.sessions) < initial_len


def test_player_has_multiple_sessions():
    repo = FakeSessionRepo()
    sessions = repo.list_sessions_by_player(1)

    assert len(sessions) > 1


