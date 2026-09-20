"""
MongoDB Repository for EduPath Learner Profiles.

Handles database persistence for the 'learner_profiles' collection with user_id indexing
and safe upsert operations directly against MongoDB.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional
from app.core.database import DatabaseConnectionError, db_manager

logger = logging.getLogger("edupath.profile_repository")


class ProfileRepository:
    """Data access repository for MongoDB learner_profiles collection."""

    COLLECTION_NAME = "learner_profiles"

    def _get_collection(self):
        """Returns PyMongo collection or raises DatabaseConnectionError if database is disconnected."""
        if db_manager.db is None:
            raise DatabaseConnectionError("MongoDB connection is unavailable.")
        return db_manager.db[self.COLLECTION_NAME]

    def ensure_indexes(self) -> None:
        """Creates indexes on learner_profiles collection if MongoDB is available."""
        if db_manager.db is None:
            return
        try:
            collection = self._get_collection()
            collection.create_index("user_id", unique=True)
            logger.info("Created unique index on 'user_id' in 'learner_profiles' collection.")
        except Exception as err:
            logger.warning(f"Failed to create index on 'learner_profiles': {str(err)}")

    def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a learner profile document by user_id from MongoDB.
        Raises DatabaseConnectionError if MongoDB is unavailable.
        """
        collection = self._get_collection()
        try:
            return collection.find_one({"user_id": user_id}, {"_id": 0})
        except DatabaseConnectionError:
            raise
        except Exception as err:
            logger.error(f"Error fetching profile for user_id '{user_id}': {str(err)}")
            raise DatabaseConnectionError(f"Database query failed: {str(err)}") from err

    def save_profile(self, profile_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upserts (creates or updates) a learner profile document directly in MongoDB.
        Sets created_at on insert and updated_at on every save.
        Raises DatabaseConnectionError if MongoDB is unavailable.
        """
        collection = self._get_collection()
        user_id = profile_dict.get("user_id")

        if not user_id:
            raise ValueError("profile_dict must contain a valid 'user_id'")

        now = datetime.utcnow().isoformat()
        profile_dict["updated_at"] = now

        try:
            existing = collection.find_one({"user_id": user_id})
            if existing and "created_at" in existing:
                profile_dict["created_at"] = existing["created_at"]
            else:
                profile_dict["created_at"] = now

            collection.update_one(
                {"user_id": user_id},
                {"$set": profile_dict},
                upsert=True,
            )
            logger.info(f"Successfully saved profile for user_id '{user_id}' in MongoDB.")
            saved = collection.find_one({"user_id": user_id}, {"_id": 0})
            return saved or profile_dict
        except DatabaseConnectionError:
            raise
        except Exception as err:
            logger.error(f"Failed to save profile for user_id '{user_id}' in MongoDB: {str(err)}")
            raise DatabaseConnectionError(f"Database write operation failed: {str(err)}") from err


profile_repository = ProfileRepository()
