from fastapi import FastAPI, APIRouter, Depends
from anchor_academy.apis.dependencies import get_player_service, get_session_service
from anchor_academy.apis.routers import players, sessions


#create an instance of an app, or the FastAPI class
app = FastAPI(title="Anchor Academy API", description="API for Anchor Academy Player Tracking", version="1.0.0")
app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])


#Define an Endpoint/path for the root path
"""
@app.get("/")
def root():
    return {"message": "Hello, World!"}
"""


@app.get("/players")
def list_players(player_service=Depends(get_player_service)):
    """
    Endpoint to list all players in the database.
    """
    players = player_service.list_players()
    return players

@app.get("/sessions")
def list_sessions(session_service=Depends(get_session_service)):
    """
    Endpoint to list all sessions in the database.
    """
    sessions = session_service.list_sessions()
    return sessions

@app.get("/players/{player_id}/sessions")
def list_player_sessions(player_id: int, session_service=Depends(get_session_service)):
    """
    Endpoint to list all sessions for a specific player in the database.
    """
    sessions = session_service.list_player_sessions(player_id)
    return sessions