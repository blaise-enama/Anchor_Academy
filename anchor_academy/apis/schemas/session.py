from pydantic import BaseModel, field_serializer
from datetime import date, datetime
from typing import Union


class SessionCreate(BaseModel):
    player_id: int
    session_date: str  # "YYYY-MM-DD" — parsed inside the service, keep as str here
    duration_minutes: int
    sprint_count: int
    total_distance: float
    max_speed: float
    touches_left: int
    touches_right: int

    # whatever attributes a session needs at creation time

class SessionResponse(BaseModel):
    session_id: int
    player_id: int
    session_date: Union[datetime, date]
    duration_minutes: int
    sprint_count: int
    total_distance: float
    max_speed: float
    touches_left: int
    touches_right: int
    dominant_foot: str | None = None  # Optional, can be calculated based on touches_left and touches_right
    
    @field_serializer("session_date")
    def serialize_session_date(self, session_date: Union[datetime, date], _info) -> str:
        if isinstance(session_date, datetime):
            return session_date.strftime("%Y-%m-%d")
        return session_date.strftime("%Y-%m-%d")


    class Config:
        from_attributes = True # Read from a Session object's attributes