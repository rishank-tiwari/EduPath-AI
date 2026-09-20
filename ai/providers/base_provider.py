"""
Abstract AI Provider Interface for EduPath.

Provides a decoupled abstraction over LLM backends (OpenAI, Anthropic, Gemini, local LLMs).
Agents interact exclusively with this provider interface rather than vendor SDKs directly.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, Optional, Type
from pydantic import BaseModel


class BaseAIProvider(ABC):
    """Abstract Base Class for LLM Providers."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate text completion from prompt.
        
        Raises NotImplementedError if invoked before provider implementation.
        """
        pass

    @abstractmethod
    async def generate_structured(
        self, prompt: str, response_model: Type[BaseModel], system_prompt: Optional[str] = None, **kwargs
    ) -> BaseModel:
        """
        Generate structured output adhering to a Pydantic schema.
        
        Raises NotImplementedError if invoked before provider implementation.
        """
        pass

    @abstractmethod
    async def stream(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream text response chunks.
        
        Raises NotImplementedError if invoked before provider implementation.
        """
        pass
