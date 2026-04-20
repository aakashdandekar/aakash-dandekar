"""Database connection and initialisation."""
from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import settings

client = None

def get_db() -> Database:
    global client
    if client is None:
        client = MongoClient(settings.MONGO_URI)
    return client[settings.DB_NAME]

def init_db() -> None:
    from .seed import seed_if_empty
    db = get_db()
    seed_if_empty(db)
