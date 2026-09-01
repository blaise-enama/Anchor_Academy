# anchor_academy/apis/routers/sessions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from anchor_academy.apis.dependencies import get_session_service
from anchor_academy.apis.schemas import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/", response_model=SessionResponse, status_code=201)
def add_session(payload: SessionCreate, service=Depends(get_session_service)):
    try:
        session = service.add_session(
            player_id=payload.player_id,
            session_date=payload.session_date,
            duration_minutes=payload.duration_minutes,
            sprint_count=payload.sprint_count,
            total_distance=payload.total_distance,
            max_speed=payload.max_speed,
            touches_left=payload.touches_left,
            touches_right=payload.touches_right,
        )
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SessionResponse])
def list_sessions(service=Depends(get_session_service)):
    return service.list_sessions()


@router.get("/player", response_model=list[SessionResponse])
def list_player_sessions(
    player_id: int | None = Query(default=None),
    name: str | None = Query(default=None),
    service=Depends(get_session_service),
):
    try:
        return service.list_player_sessions(player_id=player_id, name=name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int, service=Depends(get_session_service)):
    try:
        service.delete_session(session_id)
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))