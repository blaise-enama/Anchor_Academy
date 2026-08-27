from anchor_academy.src.services.session_services import SessionService

class PlayerMetrics:
    def __init__(self, session_service: SessionService):
        self.sessionService = session_service

    def build_session_report(session):
        return {
        "session_id": session.session_id,
        "date": session.session_date,
        "distance": session.total_distance,
        "sprints": session.sprint_count,
        "max_speed": session.max_speed,
        "touches_left": session.touches_left,
        "touches_right": session.touches_right,
        "dominant_foot": session.dominant_foot
    }