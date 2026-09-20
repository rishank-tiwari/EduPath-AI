"""
Base Agent Interface for EduPath.

Defines standard properties, tool registries, observability traces, and execution handlers
for all specialized sub-agents and the Orchestrator.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ai.providers.base_provider import BaseAIProvider


class AgentTrace(BaseModel):
    """Observability model capturing agent actions, inputs, decisions, and tool calls."""

    trace_id: str
    agent_name: str
    input_data: Dict[str, Any]
    decision: Optional[str] = None
    tools_used: List[str] = Field(default_factory=list)
    output_data: Optional[Dict[str, Any]] = None
    status: str = "pending"
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """Abstract Base Class for EduPath autonomous agents."""

    def __init__(
        self,
        name: str,
        description: str,
        provider: Optional[BaseAIProvider] = None,
        tools: Optional[List[Any]] = None,
    ):
        self.name = name
        self.description = description
        self.provider = provider
        self.tools = tools or []
        self._last_trace: Optional[AgentTrace] = None

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent logic given inputs.
        Must be overridden by agent implementations.
        """
        pass

    def get_last_trace(self) -> Optional[AgentTrace]:
        """Returns the most recent execution trace for telemetry and debugging."""
        return self._last_trace
