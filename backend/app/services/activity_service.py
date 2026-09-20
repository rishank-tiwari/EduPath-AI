"""
Activity Domain Service for EduPath.

Handles logging learning events and notifying progress/adaptation services when completed.
"""

from typing import Any, Dict, List, Optional
from app.repositories.activity_repository import activity_repository
from app.schemas.activity import LearningActivityCreate, LearningActivityRecord
from app.services.progress_service import progress_service
from app.utils.logger import logger


class ActivityService:
    """Domain service for managing learning activity lifecycle events."""

    async def log_activity(self, payload: LearningActivityCreate) -> LearningActivityRecord:
        """Records a learning activity and updates learner progress summaries."""
        data = payload.model_dump()
        record_dict = activity_repository.record_activity(data)

        # Update progress service summaries for completed practice or assessment
        if payload.activity_type in ("practice_completed", "assessment_completed") and payload.score is not None:
            if payload.skill_name:
                progress_service.record_event(
                    user_id=payload.user_id,
                    event_type=payload.activity_type,
                    skill_name=payload.skill_name,
                    topic=payload.topic or "General Topic",
                    metadata={"score": payload.score},
                )

        return LearningActivityRecord(**record_dict)

    def get_user_activities(self, user_id: str, limit: int = 50) -> List[LearningActivityRecord]:
        """Retrieves activity history for a learner."""
        docs = activity_repository.get_user_activities(user_id=user_id, limit=limit)
        return [LearningActivityRecord(**d) for d in docs]


activity_service = ActivityService()
