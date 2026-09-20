"""
Context-Aware AI Mentor API Endpoints (PHASE 2 TASK 2.2).
"""

from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.mentor import MentorChatRequest, MentorResponse, SanitizedMentorContext
from app.services.mentor_service import mentor_service
from app.utils.logger import logger

router = APIRouter(prefix="/mentor", tags=["Mentor"])


@router.post(
    "/chat",
    response_model=MentorResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Context-Aware AI Mentor",
    description="Sends a learner message to the AI Mentor Agent. The agent builds context from live learner state and returns a structured response.",
)
async def chat_with_mentor(request: MentorChatRequest) -> MentorResponse:
    """Handles POST /api/v1/mentor/chat requests."""
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message field cannot be empty.",
        )

    try:
        response = await mentor_service.chat(user_id=request.user_id, message=request.message)
        return response
    except Exception as err:
        logger.error(f"Error executing AI Mentor chat for user '{request.user_id}': {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Your mentor couldn't respond right now. Please try again.",
        )


@router.get(
    "/context",
    response_model=SanitizedMentorContext,
    status_code=status.HTTP_200_OK,
    summary="Get Sanitized Mentor Context",
    description="Returns the current sanitized learner context assembled from live DB records.",
)
async def get_mentor_context(
    user_id: str = Query(..., description="Learner User ID (e.g. 'demo_user_1')")
) -> SanitizedMentorContext:
    """Handles GET /api/v1/mentor/context requests."""
    try:
        context = mentor_service.get_context(user_id=user_id)
        return context
    except Exception as err:
        logger.error(f"Error fetching mentor context for user '{user_id}': {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve mentor context.",
        )
