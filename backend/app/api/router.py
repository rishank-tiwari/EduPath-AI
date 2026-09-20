"""
Centralized API Version 1 Router for EduPath.
"""

from fastapi import APIRouter
from app.api.routes import (
    activities,
    adaptation,
    auth,
    documents,
    health,
    mentor,
    plans,
    practice,
    profile,
    progress,
    projects,
    resources,
    skill_gaps,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(documents.router)
api_router.include_router(projects.router)
api_router.include_router(activities.router)
api_router.include_router(skill_gaps.router)
api_router.include_router(plans.router)
api_router.include_router(resources.router)
api_router.include_router(practice.router)
api_router.include_router(progress.router)
api_router.include_router(adaptation.router)
api_router.include_router(mentor.router)
