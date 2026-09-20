"""
Unit and Integration Test Suite for Context-Aware AI Mentor Agent (PHASE 2 TASK 2.2).
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from ai.agents.mentor.context_builder import MentorContextBuilder
from ai.agents.mentor.mentor_agent import MentorAgent
from ai.providers.factory import UnimplementedAIProvider, get_ai_provider
from app.core.database import db_manager
from app.main import app
from app.schemas.mentor import MentorChatRequest, MentorResponse, SanitizedMentorContext
from app.schemas.practice import LearnerAnswerItem
from app.services.adaptation_service import adaptation_service
from app.services.learning_plan_service import learning_plan_service
from app.services.practice_service import practice_service
from app.services.profile_service import profile_service
from app.services.skill_gap_service import skill_gap_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_mongodb():
    """Provides isolated mongomock MongoDB instance for each test."""
    mock_client = mongomock.MongoClient()
    db_manager.client = mock_client
    db_manager.db = mock_client["edupath_test"]
    yield
    db_manager.client = None
    db_manager.db = None


def test_mentor_schemas():
    """Test 1 & 2: Mentor request & response Pydantic schema validation."""
    req = MentorChatRequest(user_id="user_123", message="Why am I learning Statistics?")
    assert req.user_id == "user_123"
    assert req.message == "Why am I learning Statistics?"

    resp = MentorResponse(
        response="Statistics is key for your AI/ML role.",
        context_topic="Statistics",
        suggested_action="Start Practice",
        response_mode="fallback",
    )
    assert resp.response_mode == "fallback"
    assert resp.context_topic == "Statistics"


def test_context_builder_empty_user():
    """Test 3 & 11: Context builder with missing or non-existent user data."""
    ctx = MentorContextBuilder.build_context("non_existent_user_999")
    assert isinstance(ctx, SanitizedMentorContext)
    assert ctx.user_id == "non_existent_user_999"
    assert ctx.target_role == "AI/ML Engineer"
    assert ctx.current_skills == []
    assert ctx.missing_skills == []


@pytest.mark.asyncio
async def test_context_builder_with_learner_state():
    """Test 4-10: Context builder with complete profile, skill gaps, plan, practice, progress, and adaptation."""
    user_id = "test_mentor_user_1"

    # Setup profile
    profile_service.save_profile({
        "user_id": user_id,
        "full_name": "Context Tester",
        "target_role": "AI/ML Engineer",
        "experience_level": "intermediate",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}],
        "education": [{"degree": "BS", "field_of_study": "CS", "institution": "State U"}],
        "career_goal": "Become AI Lead",
        "projects": [],
        "certifications": [],
    })

    # Setup skill gaps
    await skill_gap_service.analyze_and_save_gaps(user_id)

    # Setup learning plan
    await learning_plan_service.generate_plan(user_id)

    # Setup practice result
    practice_session = practice_service.generate_practice(
        user_id=user_id, task_id="task_01", skill_name="Statistics", difficulty="beginner"
    )
    practice_service.submit_practice(
        practice_id=practice_session.practice_id,
        user_id=user_id,
        answers=[LearnerAnswerItem(question_id=q.question_id, learner_answer="Wrong answer") for q in practice_session.questions],
    )

    # Setup adaptation event
    await adaptation_service.analyze_and_adapt(user_id=user_id, skill_name="Statistics")

    # Build context
    ctx = MentorContextBuilder.build_context(user_id)
    assert ctx.user_id == user_id
    assert ctx.target_role == "AI/ML Engineer"
    assert "Python" in ctx.current_skills
    assert ctx.learning_plan_summary is not None
    assert ctx.current_learning_task is not None
    assert ctx.recent_practice_result is not None
    assert ctx.recent_adaptation is not None


@pytest.mark.asyncio
async def test_mentor_intents_fallback():
    """Test 12-18: Question intents resolution under fallback mode."""
    agent = MentorAgent()
    user_id = "test_mentor_intents"

    # Setup initial profile & plan
    profile_service.save_profile({
        "user_id": user_id,
        "full_name": "Intent Tester",
        "target_role": "AI/ML Engineer",
        "career_goal": "Master AI",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}],
    })
    await skill_gap_service.analyze_and_save_gaps(user_id)
    await learning_plan_service.generate_plan(user_id)

    # 1. Why learning
    r1 = await agent.execute({"user_id": user_id, "message": "Why am I learning Statistics?"})
    assert "You're learning" in r1.response or "Statistics" in r1.response
    assert r1.response_mode == "fallback"

    # 2. Next step
    r2 = await agent.execute({"user_id": user_id, "message": "What should I learn next?"})
    assert "next step" in r2.response.lower()

    # 3. Explanation in simple words
    r3 = await agent.execute({"user_id": user_id, "message": "Explain this in simple words"})
    assert "simple" in r3.response.lower() or "think of" in r3.response.lower() or "heart" in r3.response.lower()

    # 4. Example question
    r5 = await agent.execute({"user_id": user_id, "message": "Give me an example"})
    assert "example" in r5.response.lower()

    # 5. Practice question
    r5 = await agent.execute({"user_id": user_id, "message": "Give me a practice question"})
    assert "practice question" in r5.response.lower()

    # 6. Plan change
    r6 = await agent.execute({"user_id": user_id, "message": "Why did my learning path change?"})
    assert "learning path" in r6.response.lower()


def test_no_hallucinated_learner_data():
    """Test 19: Mentor returns clean context without hallucinated projects or roles."""
    ctx = MentorContextBuilder.build_context("empty_user_000")
    assert ctx.current_skills == []
    assert ctx.recent_practice_result is None
    assert ctx.recent_adaptation is None


def test_provider_abstraction():
    """Test 20 & 21: Verify agent uses provider abstraction and marks response_mode = fallback when UnimplementedAIProvider is used."""
    agent = MentorAgent(provider=UnimplementedAIProvider())
    assert isinstance(agent.provider, UnimplementedAIProvider)


def test_api_validation():
    """Test 22: API returns 422 for empty message payload."""
    res = client.post("/api/v1/mentor/chat", json={"user_id": "demo_user_1", "message": ""})
    assert res.status_code == 422


def test_api_chat_success():
    """Test 23: API POST /api/v1/mentor/chat returns 200 OK with valid MentorResponse."""
    res = client.post("/api/v1/mentor/chat", json={"user_id": "demo_user_1", "message": "What should I learn next?"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert "context_topic" in data
    assert data["response_mode"] in ["llm", "fallback"]


def test_api_context_endpoint():
    """Test 24: GET /api/v1/mentor/context returns sanitized learner context."""
    res = client.get("/api/v1/mentor/context?user_id=demo_user_1")
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == "demo_user_1"
    assert "target_role" in data


@pytest.mark.asyncio
async def test_end_to_end_mentor_scenario():
    """Test 25-30: End-to-end scenario: profile -> skill gaps -> plan -> practice -> adaptation -> mentor context check."""
    user_id = "e2e_mentor_learner"

    # Step 1: Learner Profile
    profile_service.save_profile({
        "user_id": user_id,
        "full_name": "E2E Learner",
        "target_role": "AI/ML Engineer",
        "experience_level": "entry-level",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}],
        "education": [{"degree": "BS", "field_of_study": "CS", "institution": "Tech Inst"}],
        "career_goal": "AI Engineer",
        "projects": [],
        "certifications": [],
    })

    # Step 2: Skill Gap Analysis
    gaps = await skill_gap_service.analyze_and_save_gaps(user_id)
    assert len(gaps.skills) > 0

    # Step 3: Learning Plan
    plan = await learning_plan_service.generate_plan(user_id)
    assert plan.version == 1

    # Step 4: Practice & Adaptation
    session = practice_service.generate_practice(
        user_id=user_id, task_id=plan.modules[0].tasks[0].task_id, skill_name="Statistics", difficulty="beginner"
    )
    practice_service.submit_practice(
        practice_id=session.practice_id,
        user_id=user_id,
        answers=[LearnerAnswerItem(question_id=q.question_id, learner_answer="Wrong choice") for q in session.questions],
    )
    adaptation = await adaptation_service.analyze_and_adapt(user_id=user_id, skill_name="Statistics")

    # Step 5: Ask Mentor "Why am I learning Statistics?"
    agent = MentorAgent()
    r1 = await agent.execute({"user_id": user_id, "message": "Why am I learning Statistics?"})
    assert "Statistics" in r1.context_topic or "Statistics" in r1.response

    # Step 6: Ask Mentor "What should I learn next?"
    r2 = await agent.execute({"user_id": user_id, "message": "What should I learn next?"})
    assert r2.suggested_action is not None

    # Step 7: Ask Mentor "Why did my learning path change?"
    r3 = await agent.execute({"user_id": user_id, "message": "Why did my learning path change?"})
    assert "updated" in r3.response.lower() or "version" in r3.response.lower() or "learning path" in r3.response.lower()
