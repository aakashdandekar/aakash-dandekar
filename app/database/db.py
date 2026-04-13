"""Database connection and initialisation."""
from pymongo import MongoClient
from pymongo.database import Database
from ..core.config import settings

_client = None

def get_db() -> Database:
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client[settings.DB_NAME]

def init_db() -> None:
    from .seed import seed_if_empty
    db = get_db()
    seed_if_empty(db)
