"""Base Pydantic Schemas for AI Agents."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BaseAgentInput(BaseModel):
    """Standard input container for agent calls."""

    user_id: str
    session_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class BaseAgentOutput(BaseModel):
    """Standard output container for agent execution results."""

    status: str
    data: Dict[str, Any] = Field(default_factory=dict)
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
