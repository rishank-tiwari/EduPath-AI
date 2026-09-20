"""CORS Middleware setup for EduPath FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configures CORS middleware allowing local development frontend origins."""
    origins = list(set(settings.CORS_ORIGINS + [settings.FRONTEND_URL]))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
