"""
Unit tests for EduPath Milestone: Document & Portfolio Intelligence,
Practice & Project Task Generation, Learning Activity Tracking, and Dynamic Plan Adaptation.
"""

import pytest
import os
import mongomock
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import db_manager
from ai.agents.profile.document_agent import DocumentIntelligenceAgent
from ai.agents.practice.practice_agent import PracticeAgent
from ai.agents.practice.project_agent import ProjectAgent
from ai.agents.adaptation.adaptation_agent import AdaptationAgent
from ai.agents.mentor.mentor_agent import MentorAgent
from app.services.activity_service import activity_service
from app.schemas.activity import LearningActivityCreate


@pytest.fixture(autouse=True)
def setup_mock_db():
    """Sets up in-memory mongomock database for test isolation."""
    db_manager.client = mongomock.MongoClient()
    db_manager.db = db_manager.client["edupath_test_db"]
    yield
    db_manager.client.drop_database("edupath_test_db")


client = TestClient(app)


@pytest.mark.asyncio
async def test_1_and_2_document_skill_and_evidence_extraction():
    """Requirement 1 & 2: Resume/document skill extraction with attached evidence."""
    agent = DocumentIntelligenceAgent()
    sample_resume = (
        "Experienced software developer. Built a FastAPI backend for an ML application using Python and PostgreSQL. "
        "Trained PyTorch deep learning models for classification. Implemented Docker containers and CI/CD."
    )
    result = await agent.execute({
        "text": sample_resume,
        "user_id": "test_user_doc",
        "document_type": "resume",
        "filename": "sample_resume.pdf",
    })

    assert result["user_id"] == "test_user_doc"
    assert len(result["skills"]) >= 3

    skill_names = [s["name"] for s in result["skills"]]
    assert "Python" in skill_names
    assert "FastAPI" in skill_names
    assert "PyTorch" in skill_names

    # Check evidence attached
    python_skill = next(s for s in result["skills"] if s["name"] == "Python")
    assert len(python_skill["evidence"]) > 0
    assert python_skill["evidence"][0]["verified"] is True
    assert python_skill["confidence"] >= 0.70


def test_3_and_4_and_5_practice_generation_modes():
    """Requirement 3, 4, 5: General practice = 10 questions mixed across gaps; Module practice = 5 questions."""
    agent = PracticeAgent()

    # General Practice
    gen_session = agent.generate_practice_session(
        user_id="test_user_prac",
        task_id="task_gen",
        skill_name="General",
        practice_mode="general",
        skills=["Statistics", "Probability", "Model Evaluation"],
    )

    assert len(gen_session["session_data"]["questions"]) == 10
    assert len(gen_session["full_questions"]) == 10
    for q in gen_session["session_data"]["questions"]:
        assert q["skill_name"] is not None
        assert q["topic"] is not None

    # Module Practice
    mod_session = agent.generate_practice_session(
        user_id="test_user_prac",
        task_id="task_mod",
        skill_name="Python",
        practice_mode="module",
        module_id="mod_01",
    )

    assert len(mod_session["session_data"]["questions"]) == 5
    assert len(mod_session["full_questions"]) == 5
    assert mod_session["session_data"]["module_id"] == "mod_01"


@pytest.mark.asyncio
async def test_6_project_generation_uses_skill_gaps():
    """Requirement 6: Project generation uses identified skill gaps and target role."""
    agent = ProjectAgent()
    result = await agent.execute({
        "target_role": "AI/ML Engineer",
        "skill_gaps": ["Statistics", "Model Evaluation"],
        "experience_level": "Entry-Level",
    })

    projects = result["projects"]
    assert len(projects) >= 1
    p1 = projects[0]
    assert "title" in p1
    assert "objective" in p1
    assert "skills_practiced" in p1
    assert "difficulty" in p1
    assert "estimated_duration" in p1
    assert "suggested_tech_stack" in p1


@pytest.mark.asyncio
async def test_7_activity_completion_persisted():
    """Requirement 7: Activity completion is persisted in activity service."""
    activity_payload = LearningActivityCreate(
        user_id="test_user_act",
        activity_type="practice_completed",
        activity_id="prac_101",
        skill_name="Statistics",
        topic="Probability Basics",
        status="completed",
        score=85.0,
    )
    record = await activity_service.log_activity(activity_payload)
    assert record.user_id == "test_user_act"
    assert record.score == 85.0

    history = activity_service.get_user_activities("test_user_act")
    assert len(history) >= 1
    assert history[0].activity_type == "practice_completed"


def test_8_9_10_adaptation_decisions_and_plan_version():
    """Requirement 8, 9, 10: Low score triggers review/adaptation, high score advances learner, version increments."""
    agent = AdaptationAgent()
    base_plan = {
        "plan_id": "plan_01",
        "user_id": "test_user_adapt",
        "version": 1,
        "modules": [
            {
                "module_id": "mod_stat",
                "title": "Statistics Foundations",
                "skill_name": "Statistics",
                "status": "in_progress",
                "tasks": [{"task_id": "t1", "title": "Intro Stat"}],
            }
        ],
    }

    # Low score test (<60%)
    low_prog = {
        "user_id": "test_user_adapt",
        "skill_name": "Statistics",
        "topic": "Probability Basics",
        "performance_status": "struggling",
        "latest_score": 40.0,
    }
    low_decision, updated_plan_low = agent.adapt_learning_plan(base_plan, low_prog)
    assert low_decision.action == "review"
    assert low_decision.new_plan_version == 2
    assert updated_plan_low["version"] == 2
    assert len(updated_plan_low["modules"][0]["tasks"]) > 1

    # High score test (>=80%)
    high_prog = {
        "user_id": "test_user_adapt",
        "skill_name": "Statistics",
        "topic": "Probability Basics",
        "performance_status": "strong",
        "latest_score": 90.0,
    }
    high_decision, updated_plan_high = agent.adapt_learning_plan(base_plan, high_prog)
    assert high_decision.action == "move_forward"
    assert high_decision.new_plan_version == 2


@pytest.mark.asyncio
async def test_11_and_12_mentor_context_and_gemini_key_privacy():
    """Requirement 11 & 12: Mentor receives updated learner context, Gemini key is never in frontend response."""
    agent = MentorAgent()
    res = await agent.execute({
        "user_id": "demo_user_1",
        "message": "Why am I learning Statistics?",
    })

    assert res.response is not None
    assert "Statistics" in res.response or "Statistics" in res.context_topic
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if gemini_key:
        assert gemini_key not in res.response
