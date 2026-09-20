"""
AI Provider Factory for EduPath.

Instantiates configured LLM provider drivers based on environment settings.
"""

import os
from typing import Optional
from ai.providers.base_provider import BaseAIProvider
from ai.providers.gemini_provider import GeminiProvider
from app.core.config import settings


class UnimplementedAIProvider(BaseAIProvider):
    """Placeholder provider used when LLM drivers or API keys are unconfigured."""

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        raise NotImplementedError("LLM Provider generate capability fallback.")

    async def generate_structured(
        self, prompt: str, response_model: type, system_prompt: Optional[str] = None, **kwargs
    ):
        raise NotImplementedError("LLM Provider structured output capability fallback.")

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs):
        raise NotImplementedError("LLM Provider stream capability fallback.")
        yield ""


def get_ai_provider(provider_name: Optional[str] = None, api_key: Optional[str] = None) -> BaseAIProvider:
    """
    Returns an instance of BaseAIProvider.
    Uses GeminiProvider when LLM_PROVIDER=gemini and GEMINI_API_KEY is configured in backend settings/environment.
    """
    p_name = (provider_name or os.getenv("LLM_PROVIDER") or getattr(settings, "LLM_PROVIDER", "gemini")).lower()
    
    if api_key:
        key = api_key
    elif "GEMINI_API_KEY" in os.environ:
        key = os.environ.get("GEMINI_API_KEY") or None
    elif "LLM_API_KEY" in os.environ:
        key = os.environ.get("LLM_API_KEY") or None
    else:
        key = None

    model = os.getenv("GEMINI_MODEL") or getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")
    if not model or "1.5" in model:
        model = "gemini-3.6-flash"

    if p_name in ("gemini", "google") and key:
        return GeminiProvider(api_key=key, model=model)

    return UnimplementedAIProvider(api_key=key)
