from multiprocessing.dummy import connection

import pymysql
import os
from dotenv import load_dotenv
from anchor_academy.src.repositories.playerRepo import PlayerRepository
from anchor_academy.src.services.player_service import PlayerService
from anchor_academy.src.repositories.sessionRepo import SessionRepository
from anchor_academy.src.services.session_services import SessionService

load_dotenv()


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "anchor_academy"),
        cursorclass=pymysql.cursors.DictCursor
    )


def get_player_service() -> PlayerService:
    connection = get_db_connection()
    # Create instances of the repositories
    player_repo = PlayerRepository(connection)
    session_repo = SessionRepository(connection)
    
    # Create an instance of the service with the repositories
    player_service = PlayerService(player_repo, session_repo)
    
    return player_service

def get_session_service() -> SessionService:
    connection = get_db_connection()
    # Create instances of the repositories
    session_repo = SessionRepository(connection)
    
    # Create an instance of the service with the repositories
    session_service = SessionService(session_repo)
    
    return session_service
