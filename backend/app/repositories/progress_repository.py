"""
MongoDB Repository for EduPath Progress Summaries & Progress Events.
"""

from typing import Any, Dict, List, Optional
from pymongo import ASCENDING, DESCENDING
from app.core.database import DatabaseConnectionError, db_manager
from app.utils.logger import logger


class ProgressRepository:
    """Manages CRUD operations for progress and progress_events collections in MongoDB."""

    @property
    def progress_collection(self):
        """Returns progress collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["progress"]

    @property
    def events_collection(self):
        """Returns progress_events collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["progress_events"]

    def ensure_indexes(self) -> None:
        """Creates indexes for progress and progress_events collections."""
        try:
            self.progress_collection.create_index([("user_id", ASCENDING), ("skill_name", ASCENDING), ("topic", ASCENDING)], unique=True)
            self.progress_collection.create_index([("user_id", ASCENDING)])
            self.events_collection.create_index([("event_id", ASCENDING)], unique=True)
            self.events_collection.create_index([("user_id", ASCENDING)])
            self.events_collection.create_index([("created_at", DESCENDING)])
            logger.info("MongoDB progress collections indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Could not create indexes on progress collections: {e}")

    def save_summary(self, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves or updates a ProgressSummary document in MongoDB."""
        user_id = summary_data.get("user_id")
        skill = summary_data.get("skill_name")
        topic = summary_data.get("topic")

        if not user_id or not skill or not topic:
            raise ValueError("user_id, skill_name, and topic are required to save a progress summary.")

        query = {"user_id": user_id, "skill_name": skill, "topic": topic}
        try:
            self.progress_collection.replace_one(query, summary_data, upsert=True)
            logger.info(f"Successfully saved progress summary for user '{user_id}', skill '{skill}', topic '{topic}' in MongoDB.")
            return summary_data
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving progress summary: {e}")
            raise DatabaseConnectionError(f"Failed to save progress summary in MongoDB: {str(e)}")

    def get_summary(self, user_id: str, skill_name: str, topic: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single progress summary by user_id, skill_name, and topic."""
        try:
            doc = self.progress_collection.find_one(
                {"user_id": user_id, "skill_name": skill_name, "topic": topic}, {"_id": 0}
            )
            return doc
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching progress summary: {e}")
            raise DatabaseConnectionError(f"Failed to fetch progress summary from MongoDB: {str(e)}")

    def get_user_summaries(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all progress summary records for a user."""
        try:
            cursor = self.progress_collection.find({"user_id": user_id}, {"_id": 0})
            return list(cursor)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user progress summaries for '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch user progress summaries from MongoDB: {str(e)}")

    def save_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a ProgressEvent record in MongoDB."""
        event_id = event_data.get("event_id")
        if not event_id:
            raise ValueError("event_id is required to save a progress event.")

        try:
            self.events_collection.replace_one({"event_id": event_id}, event_data, upsert=True)
            logger.info(f"Successfully saved progress event '{event_id}' in MongoDB.")
            return event_data
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving progress event: {e}")
            raise DatabaseConnectionError(f"Failed to save progress event in MongoDB: {str(e)}")

    def get_event_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all progress events for a user sorted by created_at desc."""
        try:
            cursor = self.events_collection.find({"user_id": user_id}, {"_id": 0}).sort("created_at", DESCENDING)
            return list(cursor)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching progress history for user '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch progress history from MongoDB: {str(e)}")


progress_repository = ProgressRepository()
