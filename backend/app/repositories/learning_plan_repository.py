"""
MongoDB Repository for EduPath Learning Plans.

Provides database interaction layer for storing and retrieving personalized learning plans.
"""

from typing import Any, Dict, Optional
from pymongo import ASCENDING
from app.core.database import DatabaseConnectionError, db_manager
from app.utils.logger import logger


class LearningPlanRepository:
    """Manages CRUD persistence operations for the learning_plans collection in MongoDB."""

    @property
    def collection(self):
        """Returns the learning_plans PyMongo collection or raises DatabaseConnectionError."""
        if db_manager.db is None:
            logger.error("MongoDB database is not initialized or disconnected.")
            raise DatabaseConnectionError("MongoDB database connection is unavailable.")
        return db_manager.db["learning_plans"]

    def ensure_indexes(self) -> None:
        """Creates indexes for optimized user_id and plan_id queries."""
        try:
            self.collection.create_index([("user_id", ASCENDING)], unique=True)
            self.collection.create_index([("plan_id", ASCENDING)], unique=True)
            self.collection.create_index([("target_role", ASCENDING)])
            logger.info("MongoDB learning_plans collection indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Could not create indexes on learning_plans collection: {e}")

    def save_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Saves or updates a personalized learning plan document in MongoDB.
        Performs an upsert based on user_id.
        """
        user_id = plan_data.get("user_id")
        if not user_id:
            raise ValueError("user_id is required to save a learning plan.")

        try:
            coll = self.collection
            coll.replace_one({"user_id": user_id}, plan_data, upsert=True)
            logger.info(f"Successfully saved learning plan for user_id '{user_id}' in MongoDB.")
            return plan_data
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error saving learning plan for user '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to save learning plan in MongoDB: {str(e)}")

    def get_latest_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the current/latest learning plan document for a given user_id."""
        try:
            plan = self.collection.find_one({"user_id": user_id}, {"_id": 0})
            return plan
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching learning plan for user '{user_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch learning plan from MongoDB: {str(e)}")

    def get_by_plan_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific learning plan document by plan_id."""
        try:
            plan = self.collection.find_one({"plan_id": plan_id}, {"_id": 0})
            return plan
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Error fetching learning plan for plan_id '{plan_id}': {e}")
            raise DatabaseConnectionError(f"Failed to fetch learning plan from MongoDB: {str(e)}")


learning_plan_repository = LearningPlanRepository()
