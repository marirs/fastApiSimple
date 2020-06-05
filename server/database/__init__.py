"""
- Database adapters
- Database Models
- CRUD operations
"""
from .crud.user import UserDatabase
from .models.user import User
from server.config import Config
from server.database.mongodb import AsyncIOMotorClient, get_database

__all__ = [
    "get_userdb"
]


async def get_userdb() -> UserDatabase:
    db_client: AsyncIOMotorClient = await get_database()
    users_collection = db_client[Config.DB_NAME][Config.USERS_DOCUMENT_NAME]
    return UserDatabase(User, users_collection)


