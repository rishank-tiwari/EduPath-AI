"""Base Agent Memory interface for EduPath."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseMemory(ABC):
    """Abstract Base Class for stateful agent memory management."""

    @abstractmethod
    async def add_entry(self, session_id: str, role: str, content: Any) -> None:
        """Add a memory observation or interaction entry."""
        pass

    @abstractmethod
    async def get_history(self, session_id: str, limit: int = 10) -> List[Any]:
        """Fetch historical memory context for a session."""
        pass

    @abstractmethod
    async def clear(self, session_id: str) -> None:
        """Clear session memory."""
        pass
