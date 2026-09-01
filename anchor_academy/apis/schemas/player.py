from pydantic import BaseModel


"""
this is the domain model for the player object. 
It defines the attributes of a player and their data types. 
The PlayerCreate class is used for creating new players, while the PlayerResponse class is used for returning player data in API responses.
"""
class PlayerCreate(BaseModel):
    # Schema for creating a new player, defines the attributes and their types
    name: str
    position: str
    age: int
    team: str
    sessions: list | None = []

class PlayerResponse(BaseModel):
    # Schema for returning player data in API responses, includes the player ID
    id: int
    name: str
    position: str
    age: int
    team: str

    class Config:
        orm_mode = True #Lets you rerturn the domain object