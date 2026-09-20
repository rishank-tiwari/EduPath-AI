"""
Skill Gap Service for EduPath.

Coordinates Learner Profile retrieval, Skill Gap Agent execution, and MongoDB persistence.
"""

from typing import Optional
from ai.agents.skill_gap.skill_gap_agent import SkillGapAgent
from ai.schemas.skill_gap_schema import SkillGapAnalysisResult
from app.repositories.skill_gap_repository import skill_gap_repository
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse
from app.services.profile_service import profile_service
from app.utils.skill_normalizer import normalize_skill_name


class SkillGapService:
    """Domain service managing skill gap analysis operations and Skill Gap Agent executions."""

    def __init__(self, agent: Optional[SkillGapAgent] = None):
        self.agent = agent or SkillGapAgent()

    def get_analysis(self, user_id: str) -> Optional[SkillGapResponse]:
        """Fetches stored skill gap analysis for user_id."""
        data = skill_gap_repository.get_by_user_id(user_id)
        if data:
            return SkillGapResponse(**data)
        return None

    def get_skill_analysis(self, user_id: str, skill_name: str) -> Optional[SkillGapItem]:
        """Fetches skill gap item analysis for a specific skill name."""
        analysis = self.get_analysis(user_id)
        if not analysis:
            return None

        norm_query = normalize_skill_name(skill_name).lower()
        for item in analysis.skills:
            if normalize_skill_name(item.skill_name).lower() == norm_query:
                return item
        return None

    async def analyze_and_save_gaps(self, user_id: str) -> SkillGapResponse:
        """
        Runs Skill Gap Agent analysis against stored LearnerProfile for user_id,
        calculates gap classifications, priorities, and readiness, persists in MongoDB, and returns result.
        """
        # 1. Fetch Learner Profile from Task 1.1 Profile Service
        profile = profile_service.get_profile(user_id)
        if not profile:
            raise ValueError(f"Learner profile for user_id '{user_id}' not found. Learner profile is required before skill-gap analysis.")

        if not profile.target_role or not profile.target_role.strip():
            raise ValueError(f"Learner profile for user_id '{user_id}' does not have a valid target_role specified.")

        # 2. Execute Skill Gap Agent Analysis
        analysis_result: SkillGapAnalysisResult = await self.agent.execute(profile)

        # 3. Persist Analysis Document in MongoDB
        dict_payload = analysis_result.model_dump()
        saved_dict = skill_gap_repository.save_analysis(dict_payload)

        return SkillGapResponse(**saved_dict)


skill_gap_service = SkillGapService()
