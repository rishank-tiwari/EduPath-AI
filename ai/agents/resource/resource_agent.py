"""
Resource Agent for EduPath (ACT phase).

Discovers, ranks, and curates learning resources matching specific learning tasks and skill gaps.
"""

from typing import Any, Dict
from ai.agents.base_agent import BaseAgent
from app.schemas.resource import ResourceRecommendationResponse
from app.services.resource_catalog import get_curated_resources
from app.utils.logger import logger


class ResourceAgent(BaseAgent):
    """
    Recommends curated, difficulty-matched learning materials (documentation, courses, videos, articles)
    for a target learning task.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="ResourceAgent",
            description="Recommends curated learning materials matching current skill gaps and task requirements.",
            provider=provider,
        )

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes resource recommendation logic for a given learning task.
        inputs expected:
        - task_id: str
        - skill_name: str
        - difficulty: str (optional, default 'beginner')
        """
        task_id = inputs.get("task_id") or "task_unknown"
        skill_name = inputs.get("skill_name") or "General Engineering"
        difficulty = inputs.get("difficulty") or "beginner"

        logger.info(f"ResourceAgent searching curated materials for task '{task_id}', skill '{skill_name}', difficulty '{difficulty}'...")

        resources = get_curated_resources(skill_name=skill_name, difficulty=difficulty)

        response = ResourceRecommendationResponse(
            task_id=task_id,
            skill_name=skill_name,
            topic=f"{skill_name} Learning Resources",
            resources=resources,
        )

        return response.model_dump()
