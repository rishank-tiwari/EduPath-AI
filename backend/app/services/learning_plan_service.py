"""
Learning Plan Domain Service for EduPath.

Coordinates Learner Profile ingestion, Skill Gap Analysis consumption, Role Requirements lookup,
Planner Agent execution, and Repository persistence.
"""

from typing import Optional
from fastapi import HTTPException, status
from ai.agents.learning_planner.learning_planner_agent import LearningPlannerAgent
from app.repositories.learning_plan_repository import learning_plan_repository
from app.schemas.learning_plan import LearningPlanResponse
from app.services.profile_service import profile_service
from app.services.role_service import role_service
from app.services.skill_gap_service import skill_gap_service
from app.utils.logger import logger


class LearningPlanService:
    """Domain service orchestrating personalized learning plan generation and retrieval."""

    def __init__(self):
        self.agent = LearningPlannerAgent()

    async def generate_plan(self, user_id: str) -> LearningPlanResponse:
        """
        Generates a personalized learning plan for user_id.
        Fails with 400 Bad Request if learner profile or skill gap analysis does not exist.
        """
        # 1. Fetch Learner Profile (Dependency Check)
        profile = profile_service.get_profile(user_id)
        if not profile:
            logger.warning(f"Plan generation failed: Profile not found for user '{user_id}'.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Learner profile for user_id '{user_id}' not found. Learner profile is required before generating a learning plan.",
            )

        # 2. Fetch Skill Gap Analysis (Dependency Check)
        gap_analysis = skill_gap_service.get_analysis(user_id)
        if not gap_analysis:
            logger.warning(f"Plan generation failed: Skill gap analysis not found for user '{user_id}'.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Skill gap analysis for user_id '{user_id}' not found. Skill gap analysis is required before generating a learning plan.",
            )

        # 3. Load Role Benchmark Requirements
        target_role = gap_analysis.target_role or profile.target_role
        role_reqs = role_service.get_role_requirements(target_role)

        # 4. Execute LearningPlannerAgent
        plan_dict = await self.agent.execute({
            "learner_profile": profile,
            "skill_gap_analysis": gap_analysis,
            "role_requirements": role_reqs,
        })

        # 5. Persist Plan to MongoDB
        saved_dict = learning_plan_repository.save_plan(plan_dict)
        return LearningPlanResponse(**saved_dict)

    def get_plan(self, user_id: str) -> LearningPlanResponse:
        """Retrieves the latest personalized learning plan for user_id."""
        plan_dict = learning_plan_repository.get_latest_by_user_id(user_id)
        if not plan_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning plan for user_id '{user_id}' not found.",
            )
        return LearningPlanResponse(**plan_dict)

    def get_plan_by_id(self, plan_id: str) -> LearningPlanResponse:
        """Retrieves a specific learning plan by plan_id."""
        plan_dict = learning_plan_repository.get_by_plan_id(plan_id)
        if not plan_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning plan with plan_id '{plan_id}' not found.",
            )
        return LearningPlanResponse(**plan_dict)


learning_plan_service = LearningPlanService()
