"""
MongoDB Repository for EduPath Skill Gap Analyses.

Handles database persistence for the 'skill_gaps' collection with user_id indexing
and safe upsert operations directly against MongoDB.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional
from app.core.database import DatabaseConnectionError, db_manager

logger = logging.getLogger("edupath.skill_gap_repository")


class SkillGapRepository:
    """Data access repository for MongoDB skill_gaps collection."""

    COLLECTION_NAME = "skill_gaps"

    def _get_collection(self):
        """Returns PyMongo collection or raises DatabaseConnectionError if database is disconnected."""
        if db_manager.db is None:
            raise DatabaseConnectionError("MongoDB connection is unavailable.")
        return db_manager.db[self.COLLECTION_NAME]

    def ensure_indexes(self) -> None:
        """Creates unique index on 'user_id' in skill_gaps collection if MongoDB is available."""
        if db_manager.db is None:
            return
        try:
            collection = self._get_collection()
            collection.create_index("user_id", unique=True)
            logger.info("Created unique index on 'user_id' in 'skill_gaps' collection.")
        except Exception as err:
            logger.warning(f"Failed to create index on 'skill_gaps': {str(err)}")

    def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the latest skill gap analysis document for a user_id from MongoDB.
        Raises DatabaseConnectionError if MongoDB is unavailable.
        """
        collection = self._get_collection()
        try:
            return collection.find_one({"user_id": user_id}, {"_id": 0})
        except DatabaseConnectionError:
            raise
        except Exception as err:
            logger.error(f"Error fetching skill gap analysis for user_id '{user_id}': {str(err)}")
            raise DatabaseConnectionError(f"Database query failed: {str(err)}") from err

    def save_analysis(self, analysis_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upserts (creates or updates) a skill gap analysis document directly in MongoDB.
        Sets created_at on insert and updated_at on every save.
        Raises DatabaseConnectionError if MongoDB is unavailable.
        """
        collection = self._get_collection()
        user_id = analysis_dict.get("user_id")

        if not user_id:
            raise ValueError("analysis_dict must contain a valid 'user_id'")

        now = datetime.utcnow().isoformat()
        analysis_dict["updated_at"] = now

        try:
            existing = collection.find_one({"user_id": user_id})
            if existing and "created_at" in existing:
                analysis_dict["created_at"] = existing["created_at"]
            else:
                analysis_dict["created_at"] = now

            collection.update_one(
                {"user_id": user_id},
                {"$set": analysis_dict},
                upsert=True,
            )
            logger.info(f"Successfully saved skill gap analysis for user_id '{user_id}' in MongoDB.")
            saved = collection.find_one({"user_id": user_id}, {"_id": 0})
            return saved or analysis_dict
        except DatabaseConnectionError:
            raise
        except Exception as err:
            logger.error(f"Failed to save skill gap analysis for user_id '{user_id}' in MongoDB: {str(err)}")
            raise DatabaseConnectionError(f"Database write operation failed: {str(err)}") from err


skill_gap_repository = SkillGapRepository()
