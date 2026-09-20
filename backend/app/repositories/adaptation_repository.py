"""
MongoDB Repository for EduPath Adaptation Decisions & History.
"""

from typing import Any, Dict, List
from pymongo import ASCENDING, DESCENDING
from app.core.database import DatabaseConnectionError, db_manager
from app.utils.logger import logger


class AdaptationRepository:
    """Manages CRUD operations for adaptation_events collection in MongoDB."""

    @property
    def collection(self):
        """Returns adaptation_events collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["adaptation_events"]

    def ensure_indexes(self) -> None:
        """Creates indexes for adaptation_events collection."""
        try:
            self.collection.create_index([("event_id", ASCENDING)], unique=True)
            self.collection.create_index([("user_id", ASCENDING)])
            self.collection.create_index([("created_at", DESCENDING)])
            logger.info("MongoDB adaptation_events collection indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Could not create indexes on adaptation_events collection: {e}")

    def save_adaptation(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves an AdaptationDecision document in MongoDB."""
        event_id = decision_data.get("event_id")
        if not event_id:
            raise ValueError("event_id is required to save an adaptation decision.")

        try:
            self.collection.replace_one({"event_id": event_id}, decision_data, upsert=True)
            logger.info(f"Successfully saved adaptation event '{event_id}' for user '{decision_data.get('user_id')}' in MongoDB.")
            return decision_data
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving adaptation decision: {e}")
            raise DatabaseConnectionError(f"Failed to save adaptation decision in MongoDB: {str(e)}")

    def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all previous adaptation decisions for user_id sorted by created_at desc."""
        try:
            cursor = self.collection.find({"user_id": user_id}, {"_id": 0}).sort("created_at", DESCENDING)
            return list(cursor)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching adaptation history for user '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch adaptation history from MongoDB: {str(e)}")


adaptation_repository = AdaptationRepository()
