"""
Profile Service for EduPath.

Coordinates profile retrieval, Profile Agent analysis, and MongoDB persistence.
"""

from typing import Any, Dict, Optional
from ai.agents.profile.profile_agent import ProfileAgent
from ai.schemas.profile_schema import ProfileAnalysisInput, ProfileAnalysisResult
from app.repositories.profile_repository import profile_repository
from app.schemas.learner_profile import LearnerProfileCreate, LearnerProfileResponse


def calculate_profile_completeness(payload: LearnerProfileCreate) -> float:
    """Calculates quantitative completeness score (0.0 to 100.0%) for a learner profile."""
    score = 0.0
    if payload.target_role and payload.target_role.strip():
        score += 20.0
    if payload.career_goal and payload.career_goal.strip():
        score += 20.0
    if payload.technical_skills:
        score += min(25.0, len(payload.technical_skills) * 5.0)
    if payload.projects:
        score += min(20.0, len(payload.projects) * 10.0)
    if payload.education:
        score += 10.0
    if payload.certifications:
        score += 5.0
    return min(100.0, round(score, 1))


class ProfileService:
    """Domain service managing learner profiles and Profile Agent executions."""

    def __init__(self, agent: Optional[ProfileAgent] = None):
        self.agent = agent or ProfileAgent()

    def get_profile(self, user_id: str) -> Optional[LearnerProfileResponse]:
        """Fetches stored profile for user_id."""
        data = profile_repository.get_by_user_id(user_id)
        if data:
            return LearnerProfileResponse(**data)
        return None

    def save_profile(self, payload: Any) -> LearnerProfileResponse:
        """Saves or updates learner profile in MongoDB."""
        if isinstance(payload, dict):
            payload = LearnerProfileCreate(**payload)

        if payload.profile_completeness == 0.0:
            payload.profile_completeness = calculate_profile_completeness(payload)

        dict_payload = payload.model_dump()
        saved_dict = profile_repository.save_profile(dict_payload)
        return LearnerProfileResponse(**saved_dict)

    async def analyze_and_save_profile(self, input_payload: ProfileAnalysisInput) -> LearnerProfileResponse:
        """
        Runs Profile Agent analysis against input payload, builds structured profile,
        persists to MongoDB, and returns result.
        """
        analysis_result: ProfileAnalysisResult = await self.agent.execute(input_payload)

        # Convert agent analysis result into LearnerProfileCreate model
        create_payload = LearnerProfileCreate(
            user_id=analysis_result.user_id,
            target_role=analysis_result.target_role,
            career_goal=analysis_result.career_goal,
            experience_level=analysis_result.inferred_experience_level,
            education=analysis_result.education,
            technical_skills=analysis_result.technical_skills,
            soft_skills=analysis_result.soft_skills,
            projects=analysis_result.projects,
            certifications=analysis_result.certifications,
            profile_summary=analysis_result.profile_summary,
            profile_completeness=analysis_result.profile_completeness,
        )

        return self.save_profile(create_payload)


profile_service = ProfileService()
