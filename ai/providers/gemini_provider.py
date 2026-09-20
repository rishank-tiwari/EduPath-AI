"""
Google Gemini AI Provider Implementation for EduPath.

Provides decoupled integration with Google Gemini REST API using backend environment credentials.
"""

import os
import logging
from typing import Any, AsyncGenerator, Dict, Optional, Type
import httpx
from pydantic import BaseModel
from ai.providers.base_provider import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger("edupath.gemini_provider")


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini API Provider.
    Calls backend Gemini REST endpoint asynchronously using httpx.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        key = api_key or os.getenv("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", None) or os.getenv("LLM_API_KEY")
        mdl = model or os.getenv("GEMINI_MODEL") or getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")
        if not mdl or "1.5" in mdl:
            mdl = "gemini-3.6-flash"
        super().__init__(api_key=key, model=mdl)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generates text completion using Gemini REST API.
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured in backend environment.")

        full_prompt = f"System Instruction: {system_prompt}\n\nLearner Query:\n{prompt}" if system_prompt else prompt

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": full_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 800),
            }
        }

        models_to_try = [self.model]
        if "gemini-3.6-flash" not in models_to_try:
            models_to_try.append("gemini-3.6-flash")

        last_error = None
        async with httpx.AsyncClient(timeout=30.0) as client:
            for mdl in models_to_try:
                endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={self.api_key}"
                try:
                    response = await client.post(endpoint, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        if candidates and isinstance(candidates, list):
                            cand = candidates[0]
                            content = cand.get("content", {})
                            parts = content.get("parts", [])
                            if parts and isinstance(parts, list) and len(parts) > 0:
                                text_val = parts[0].get("text", "")
                                if text_val:
                                    return text_val.strip()
                            if "text" in content:
                                return content["text"].strip()
                        logger.error(f"Gemini API returned unexpected payload for model {mdl}: {data}")
                        last_error = f"Gemini response missing valid text content for model {mdl}"
                    else:
                        logger.error(f"Gemini API Error {response.status_code} for model {mdl}: {response.text[:200]}")
                        last_error = f"Gemini API returned status {response.status_code} for model {mdl}"
                except Exception as e:
                    logger.error(f"Gemini connection error for model {mdl}: {e}")
                    last_error = str(e)

            raise RuntimeError(last_error or "Failed to connect to Gemini API")

    async def generate_structured(
        self, prompt: str, response_model: Type[BaseModel], system_prompt: Optional[str] = None, **kwargs
    ) -> BaseModel:
        """Generates structured completion adherence."""
        raw_text = await self.generate(prompt, system_prompt, **kwargs)
        return response_model.model_validate_json(raw_text)

    async def stream(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Streams completion chunks."""
        text = await self.generate(prompt, system_prompt, **kwargs)
        yield text
