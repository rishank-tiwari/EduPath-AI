"""
MongoDB Connection Infrastructure for EduPath Backend.

Handles database connection setup with PyMongo. Supports lazy connection initialization
suitable for serverless environments (Vercel) while accurately preserving DB offline error handling.
"""

import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.core.config import settings

logger = logging.getLogger("edupath.database")

class DatabaseConnectionError(Exception):
    """Raised when MongoDB connection is unreachable or disconnected."""
    pass


class Database:
    client: Optional[MongoClient] = None
    db = None
    _initialized: bool = False


db_manager = Database()


def connect_to_mongo():
    """Establishes connection to MongoDB Atlas or local MongoDB instance."""
    db_manager._initialized = True
    if not settings.MONGODB_URI:
        logger.warning("MONGODB_URI is not set. Database connection skipped.")
        return

    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI.split('@')[-1]}...")
        db_manager.client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=3000,
        )
        # Verify connection
        db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.MONGODB_DATABASE]
        logger.info(f"Successfully connected to MongoDB database: '{settings.MONGODB_DATABASE}'")
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        logger.error(f"Failed to connect to MongoDB: {str(err)}. Server will operate in database-degraded mode.")
        db_manager.client = None
        db_manager.db = None
    except Exception as err:
        logger.error(f"Unexpected database initialization error: {str(err)}")
        db_manager.client = None
        db_manager.db = None


def close_mongo_connection():
    """Closes MongoDB connection on application shutdown."""
    if db_manager.client:
        db_manager.client.close()
        logger.info("Closed MongoDB connection.")


def check_db_health() -> bool:
    """Returns True if database connection is active and healthy."""
    if not db_manager._initialized and settings.MONGODB_URI:
        connect_to_mongo()
    if db_manager.client is None:
        return False
    try:
        db_manager.client.admin.command('ping')
        return True
    except Exception:
        return False
