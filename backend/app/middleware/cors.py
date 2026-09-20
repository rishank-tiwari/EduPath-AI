"""CORS Middleware setup for EduPath FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configures CORS middleware allowing local development and production frontend origins."""
    raw_origins = settings.CORS_ORIGINS
    if isinstance(raw_origins, str):
        origins_list = [o.strip() for o in raw_origins.split(",") if o.strip()]
    elif isinstance(raw_origins, list):
        origins_list = list(raw_origins)
    else:
        origins_list = []

    if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins_list:
        origins_list.append(settings.FRONTEND_URL)

    origins_list.extend(["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"])
    origins = list(set(origins_list))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
