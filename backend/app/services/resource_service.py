"""
Resource Recommendation Domain Service for EduPath.

Coordinates learning resource discovery, agent execution, and storage.
"""

from fastapi import HTTPException, status
from ai.agents.resource.resource_agent import ResourceAgent
from app.repositories.resource_repository import resource_repository
from app.schemas.resource import ResourceRecommendationResponse
from app.utils.logger import logger


class ResourceService:
    """Domain service orchestrating resource discovery and recommendations."""

    def __init__(self):
        self.agent = ResourceAgent()

    async def recommend_resources(
        self, task_id: str, skill_name: str, difficulty: str = "beginner", user_id: str = None
    ) -> ResourceRecommendationResponse:
        """Recommends curated learning resources for a learning task."""
        if not task_id or not task_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="task_id is required to recommend learning resources.",
            )
        if not skill_name or not skill_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="skill_name is required to recommend learning resources.",
            )

        res_dict = await self.agent.execute({
            "task_id": task_id,
            "skill_name": skill_name,
            "difficulty": difficulty,
            "user_id": user_id,
        })

        # Save to database
        if res_dict.get("resources"):
            resource_repository.save_resources(res_dict["resources"])

        return ResourceRecommendationResponse(**res_dict)


resource_service = ResourceService()
