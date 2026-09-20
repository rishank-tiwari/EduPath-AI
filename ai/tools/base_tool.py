"""Base Tool interface for EduPath AI Agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract Base Class for agent tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        """Execute the tool action."""
        pass
