"""
Mentor Service Layer for EduPath Backend.

Orchestrates context building and execution of the Context-Aware AI Mentor Agent.
"""

from typing import Any, Dict
from ai.agents.mentor import MentorAgent, MentorContextBuilder
from app.schemas.mentor import MentorResponse, SanitizedMentorContext


class MentorService:
    """Service wrapping MentorAgent and MentorContextBuilder."""

    def __init__(self, agent: MentorAgent = None):
        self.agent = agent or MentorAgent()

    async def chat(self, user_id: str, message: str) -> MentorResponse:
        """Executes mentor chat interaction for user_id with message."""
        result = await self.agent.execute({"user_id": user_id, "message": message})
        return result

    def get_context(self, user_id: str) -> SanitizedMentorContext:
        """Retrieves current sanitized mentor context for user_id."""
        return MentorContextBuilder.build_context(user_id)


mentor_service = MentorService()
