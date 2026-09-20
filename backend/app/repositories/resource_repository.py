"""
MongoDB Repository for EduPath Learning Resources.
"""

from typing import Any, Dict, List, Optional
from pymongo import ASCENDING
from app.core.database import DatabaseConnectionError, db_manager
from app.utils.logger import logger


class ResourceRepository:
    """Manages CRUD persistence operations for the resources collection in MongoDB."""

    @property
    def collection(self):
        """Returns resources collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is not initialized or disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["resources"]

    def ensure_indexes(self) -> None:
        """Creates indexes for optimized resource_id and skill_name queries."""
        try:
            self.collection.create_index([("resource_id", ASCENDING)], unique=True)
            self.collection.create_index([("skill_name", ASCENDING)])
            logger.info("MongoDB resources collection indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Could not create indexes on resources collection: {e}")

    def save_resources(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Upserts a list of learning resource objects in MongoDB."""
        try:
            coll = self.collection
            for res in resources:
                res_id = res.get("resource_id")
                if res_id:
                    coll.replace_one({"resource_id": res_id}, res, upsert=True)
            return resources
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving resources: {e}")
            raise DatabaseConnectionError(f"Failed to save resources in MongoDB: {str(e)}")

    def get_by_skill(self, skill_name: str) -> List[Dict[str, Any]]:
        """Retrieves resources matching skill_name."""
        try:
            cursor = self.collection.find({"skill_name": skill_name}, {"_id": 0})
            return list(cursor)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching resources for skill '{skill_name}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch resources from MongoDB: {str(e)}")


resource_repository = ResourceRepository()
