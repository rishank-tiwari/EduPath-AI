"""
Automated tests for Phase 2 Task 2.4:
1. General Practice mixed improvement skills & module independence.
2. Gemini AI Provider abstraction and fallback handling.
3. Auth user registration, JWT login, and token verification.
"""

import os
import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from ai.providers.factory import get_ai_provider, UnimplementedAIProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.agents.mentor.mentor_agent import MentorAgent
from app.services.practice_service import PracticeService
from app.services.auth_service import auth_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_mongodb():
    """Provides isolated mongomock instance for each test."""
    mock_client = mongomock.MongoClient()
    db_manager.client = mock_client
    db_manager.db = mock_client["edupath_task_2_4_test"]
    yield
    db_manager.client = None
    db_manager.db = None


# --- GENERAL PRACTICE MIXED SKILLS TESTS ---

def test_general_practice_mixes_improvement_skills():
    """Verify general practice mixes across learner's improvement skills without module_id."""
    practice_service = PracticeService()
    session = practice_service.generate_practice(
        user_id="user_mix_skills",
        task_id="task_mix_10",
        skill_name="General",
        difficulty="beginner",
        practice_mode="general",
        skills=["Machine Learning", "Statistics", "Probability", "Model Evaluation", "MLOps"]
    )
    assert session.practice_mode == "general"
    assert session.module_id is None
    assert len(session.questions) == 10

    # Verify questions are distributed across multiple skills
    skills_found = {q.skill_name for q in session.questions if q.skill_name}
    assert len(skills_found) >= 2


# --- GEMINI PROVIDER TESTS ---

def test_gemini_provider_factory_selection():
    """Verify get_ai_provider returns GeminiProvider when LLM_PROVIDER=gemini and key is configured."""
    os.environ["LLM_PROVIDER"] = "gemini"
    os.environ["GEMINI_API_KEY"] = "fake_gemini_key_for_testing"

    provider = get_ai_provider()
    assert isinstance(provider, GeminiProvider)
    assert provider.api_key == "fake_gemini_key_for_testing"

    # Clean up environment
    os.environ.pop("GEMINI_API_KEY", None)


def test_mentor_agent_fallback_mode_when_key_missing():
    """Verify MentorAgent returns fallback mode explicitly when Gemini key is unconfigured."""
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ["LLM_PROVIDER"] = "gemini"

    agent = MentorAgent()
    assert isinstance(agent.provider, UnimplementedAIProvider) or agent.provider.api_key is None


# --- AUTHENTICATION TESTS ---

def test_auth_register_and_login_flow():
    """Verify user registration and login endpoints return valid JWT access token."""
    # 1. Register user
    reg_res = client.post("/api/v1/auth/register", json={
        "username": "testlearner",
        "email": "testlearner@edupath.ai",
        "password": "secretpassword123"
    })
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user_id"].startswith("user_")

    token = reg_data["access_token"]

    # 2. Login user
    login_res = client.post("/api/v1/auth/login", json={
        "username_or_email": "testlearner@edupath.ai",
        "password": "secretpassword123"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["access_token"] is not None

    # 3. Get /me endpoint with Bearer token
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["authenticated"] is True


def test_auth_me_requires_token():
    """Verify accessing /auth/me without Bearer token returns 401 Unauthorized."""
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
