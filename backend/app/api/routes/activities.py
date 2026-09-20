"""
API Routes for Learning Activity Tracking & Event Log.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status

from app.schemas.activity import LearningActivityCreate, LearningActivityRecord
from app.services.activity_service import activity_service
from app.services.adaptation_service import adaptation_service

router = APIRouter(prefix="/activities", tags=["Learning Activity Tracking"])


@router.post("/complete", status_code=status.HTTP_201_CREATED)
async def complete_activity(payload: LearningActivityCreate) -> Dict[str, Any]:
    """
    POST /api/v1/activities/complete
    Records a completed learning activity (practice, assessment, project, resource, mentor interaction)
    and automatically triggers performance adaptation if score is present.
    """
    record = await activity_service.log_activity(payload)

    adaptation_trigger_result = None
    if payload.score is not None and payload.activity_type in ("practice_completed", "assessment_completed"):
        try:
            adaptation_decision = await adaptation_service.analyze_and_adapt(
                user_id=payload.user_id,
                skill_name=payload.skill_name,
                topic=payload.topic,
            )
            adaptation_trigger_result = adaptation_decision.model_dump()
        except Exception:
            pass

    return {
        "status": "success",
        "activity_record": record.model_dump(),
        "adaptation_triggered": adaptation_trigger_result is not None,
        "adaptation_decision": adaptation_trigger_result,
    }


@router.get("", status_code=status.HTTP_200_OK)
async def get_activities(user_id: str = "demo_user_1", limit: int = 50) -> List[LearningActivityRecord]:
    """
    GET /api/v1/activities
    Retrieves historical learning activity events for a user.
    """
    return activity_service.get_user_activities(user_id=user_id, limit=limit)
