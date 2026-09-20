"""Base Workflow definition for EduPath Multi-Agent Graphs."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseWorkflow(ABC):
    """Abstract class for executing multi-agent graph pipelines."""

    @abstractmethod
    async def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow sequence."""
        pass
