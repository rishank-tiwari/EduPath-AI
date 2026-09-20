"""
MongoDB Connection Infrastructure for EduPath Backend.

Handles database connection setup with PyMongo. Does not crash server on startup
if database is unreachable or unconfigured during initial development phases.
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

db_manager = Database()


def connect_to_mongo():
    """Establishes connection to MongoDB Atlas or local MongoDB instance."""
    if db_manager.client is not None:
        return

    if not settings.MONGODB_URI:
        logger.warning("MONGODB_URI is not set. Initializing in-memory database store (mongomock).")
        try:
            import mongomock
            mock_client = mongomock.MongoClient()
            db_manager.client = mock_client
            db_manager.db = mock_client[settings.MONGODB_DATABASE]
            logger.info("Successfully initialized in-memory database store (mongomock).")
        except Exception as mock_err:
            logger.error(f"In-memory store initialization error: {mock_err}")
            db_manager.client = None
            db_manager.db = None
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
        logger.warning(f"Could not connect to external MongoDB ({err}). Initializing in-memory database store for serverless execution.")
        try:
            import mongomock
            mock_client = mongomock.MongoClient()
            db_manager.client = mock_client
            db_manager.db = mock_client[settings.MONGODB_DATABASE]
            logger.info("Successfully initialized in-memory database store (mongomock).")
        except Exception as mock_err:
            logger.error(f"In-memory store initialization error: {mock_err}")
            db_manager.client = None
            db_manager.db = None
    except Exception as err:
        logger.error(f"Unexpected database initialization error: {str(err)}")
        db_manager.client = None
        db_manager.db = None


def close_mongo_connection():
    """Closes MongoDB connection on application shutdown."""
    if db_manager.client:
        try:
            db_manager.client.close()
        except Exception:
            pass
        db_manager.client = None
        db_manager.db = None
        logger.info("Closed MongoDB connection.")


def check_db_health() -> bool:
    """Returns True if database connection is active and healthy."""
    if db_manager.client is None:
        return False
    try:
        if type(db_manager.client).__module__.startswith("mongomock"):
            return True
        db_manager.client.admin.command('ping')
        return True
    except Exception:
        return False
