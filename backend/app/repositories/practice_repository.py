"""
MongoDB Repository for EduPath Practice Sessions & Evaluation Results.
"""

from typing import Any, Dict, List, Optional
from pymongo import ASCENDING, DESCENDING
from app.core.database import DatabaseConnectionError, db_manager
from app.utils.logger import logger


class PracticeRepository:
    """Manages CRUD operations for practice_sessions and practice_results collections in MongoDB."""

    @property
    def sessions_collection(self):
        """Returns practice_sessions collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["practice_sessions"]

    @property
    def results_collection(self):
        """Returns practice_results collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["practice_results"]

    def ensure_indexes(self) -> None:
        """Creates indexes for practice_sessions and practice_results collections."""
        try:
            self.sessions_collection.create_index([("practice_id", ASCENDING)], unique=True)
            self.sessions_collection.create_index([("user_id", ASCENDING)])
            self.results_collection.create_index([("result_id", ASCENDING)], unique=True)
            self.results_collection.create_index([("user_id", ASCENDING)])
            self.results_collection.create_index([("practice_id", ASCENDING)])
            logger.info("MongoDB practice collections indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Could not create indexes on practice collections: {e}")

    def save_session(
        self, session_data: Dict[str, Any], full_questions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Saves an active practice session and its full questions in MongoDB."""
        practice_id = session_data.get("practice_id")
        if not practice_id:
            raise ValueError("practice_id is required to save a practice session.")

        doc = {
            "session_data": session_data,
            "full_questions": full_questions,
            "practice_id": practice_id,
            "user_id": session_data.get("user_id"),
        }

        try:
            self.sessions_collection.replace_one({"practice_id": practice_id}, doc, upsert=True)
            logger.info(f"Successfully saved practice session '{practice_id}' in MongoDB.")
            return session_data
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving practice session '{practice_id}': {e}")
            raise DatabaseConnectionError(f"Failed to save practice session in MongoDB: {str(e)}")

    def get_session(self, practice_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a practice session document by practice_id."""
        try:
            doc = self.sessions_collection.find_one({"practice_id": practice_id}, {"_id": 0})
            return doc
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching practice session '{practice_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch practice session from MongoDB: {str(e)}")

    def save_result(self, result_record: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a practice evaluation result record in MongoDB."""
        result_id = result_record.get("result_id")
        if not result_id:
            raise ValueError("result_id is required to save a practice result.")

        try:
            self.results_collection.replace_one({"result_id": result_id}, result_record, upsert=True)
            logger.info(f"Successfully saved practice result '{result_id}' for user '{result_record.get('user_id')}' in MongoDB.")
            return result_record
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving practice result: {e}")
            raise DatabaseConnectionError(f"Failed to save practice result in MongoDB: {str(e)}")

    def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all previous practice result records for a given user_id sorted by completed_at desc."""
        try:
            cursor = self.results_collection.find({"user_id": user_id}, {"_id": 0}).sort("completed_at", DESCENDING)
            return list(cursor)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching practice history for user '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch practice history from MongoDB: {str(e)}")

    def get_result(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Retrieves a practice result document by result_id or practice_id."""
        try:
            doc = self.results_collection.find_one(
                {"$or": [{"result_id": identifier}, {"practice_id": identifier}]},
                {"_id": 0},
            )
            return doc
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching practice result '{identifier}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch practice result from MongoDB: {str(e)}")


practice_repository = PracticeRepository()
