"""
MongoDB
"""
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from server.config import Config, app_logger

logger = app_logger(__name__)


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect():
    """Connect to MONGO DB
    """
    db.client = AsyncIOMotorClient(str(Config.MONGODB_URL),
                                   maxPoolSize=10,
                                   minPoolSize=10)
    try:
        db.client.server_info()
    except ServerSelectionTimeoutError:
        logger.error("Server Selection Timeout Error")
        sys.exit()
    logger.info(f"Connected to mongo at {Config.MONGODB_URL}")


async def close():
    """Close MongoDB Connection
    """
    db.client.close()
    logger.info("Closed connection with MongoDB")
