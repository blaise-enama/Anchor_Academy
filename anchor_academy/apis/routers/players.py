from fastapi import APIRouter, Depends, HTTPException
from anchor_academy.apis.dependencies import get_player_service
from anchor_academy.apis.schemas import PlayerCreate, PlayerResponse

"""
routers define the actual HTTP endpoints for the API.
A router function is intentionally designed to be a thin layer that simply receives HTTP requests, extracts the relevant data, and passes it to the service layer for processing.
The service layer contains the business logic and interacts with the repositories to perform database operations.

A router should not contain any business logic or database operations.
- Handle HTTP requests and responses
- accept Valid request data
- call the appropriate service layer functions( obtained from dependency injection)
- return the service layer's response to the client
- Translate the result/errors into an HTTP response

"""

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerResponse, status_code=201)
def add_player(player: PlayerCreate, player_service=Depends(get_player_service)):
    """
    Endpoint to add a new player to the database.
    """
    try:
        new_player = player_service.create_player(
            name=player.name,
            age=player.age,
            position=player.position,
            team=player.team
        )
        return new_player
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, player_service=Depends(get_player_service)):
    """
    Endpoint to retrieve a player by ID.
    """
    player = player_service.get_player_by_id(player_id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
