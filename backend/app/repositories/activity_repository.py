"""
MongoDB Repository for Learning Activity Tracking.
"""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime
from app.core.database import db_manager
from app.utils.logger import logger


class ActivityRepository:
    """Persistence repository for learning activity history events."""

    def __init__(self):
        self.collection_name = "learning_activities"

    def record_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a learning activity event record."""
        doc = dict(activity_data)
        if "record_id" not in doc:
            doc["record_id"] = f"act_rec_{uuid.uuid4().hex[:10]}"
        if "timestamp" not in doc:
            doc["timestamp"] = datetime.utcnow().isoformat()

        if db_manager.db is not None:
            try:
                db_manager.db[self.collection_name].insert_one(doc)
            except Exception as e:
                logger.error(f"MongoDB failed to record activity: {e}")

        # In-memory storage fallback
        if not hasattr(self, "_memory_store"):
            self._memory_store: List[Dict[str, Any]] = []
        self._memory_store.append(doc)
        return doc

    def get_user_activities(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves historical activity log for user_id."""
        if db_manager.db is not None:
            try:
                cursor = db_manager.db[self.collection_name].find(
                    {"user_id": user_id},
                    {"_id": 0}
                ).sort("timestamp", -1).limit(limit)
                results = list(cursor)
                if results:
                    return results
            except Exception as e:
                logger.error(f"MongoDB activity query error: {e}")

        # Fallback to in-memory store
        store = getattr(self, "_memory_store", [])
        filtered = [a for a in store if a.get("user_id") == user_id]
        filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return filtered[:limit]


activity_repository = ActivityRepository()
