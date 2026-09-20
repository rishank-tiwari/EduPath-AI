"""
Unit, Integration & End-to-End Tests for EduPath Progress Agent, Adaptation Agent & Adaptive Loop.
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.adaptation import AdaptationDecision
from app.schemas.progress import ProgressSummary
from ai.agents.adaptation.adaptation_agent import AdaptationAgent
from ai.agents.progress.progress_agent import ProgressAgent, classify_performance, calculate_trend

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


def test_progress_schema_and_classifications():
    """1 to 8. Test Progress schema validation and threshold classifications."""
    assert classify_performance(95.0) == "strong"
    assert classify_performance(80.0) == "on_track"
    assert classify_performance(60.0) == "needs_review"
    assert classify_performance(40.0) == "struggling"

    summary = ProgressSummary(
        progress_id="p1",
        user_id="u1",
        skill_name="Statistics",
        topic="Probability",
        latest_score=40.0,
        performance_status="struggling",
        trend="declining",
    )
    assert summary.performance_status == "struggling"


def test_trend_analysis_logic():
    """9 to 12. Test trend calculation rules."""
    assert calculate_trend([40.0]) == "insufficient_data"
    assert calculate_trend([40.0, 75.0]) == "improving"
    assert calculate_trend([80.0, 40.0]) == "declining"
    assert calculate_trend([70.0, 72.0]) == "stable"


def test_progress_recording_endpoint():
    """13. Test POST /api/v1/progress/record endpoint."""
    payload = {
        "user_id": "prog_user_01",
        "event_type": "task_completed",
        "skill_name": "Python",
        "topic": "Control Flow",
        "metadata": {"task_id": "t101"},
    }
    res = client.post("/api/v1/progress/record", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == "prog_user_01"
    assert data["event_type"] == "task_completed"


def test_adaptation_rules():
    """14 to 18. Test AdaptationAgent rule determination."""
    agent = AdaptationAgent()
    assert agent.determine_adaptation_action("strong", 95.0)[0] == "move_forward"
    assert agent.determine_adaptation_action("on_track", 80.0)[0] == "continue"
    assert agent.determine_adaptation_action("needs_review", 60.0)[0] == "add_practice"
    assert agent.determine_adaptation_action("struggling", 40.0)[0] == "review"


def test_missing_plan_adaptation_returns_400():
    """19. Test triggering adaptation without an existing plan returns 400 Bad Request."""
    res = client.post("/api/v1/adaptation/analyze", json={"user_id": "user_without_plan"})
    assert res.status_code == 400
    assert "Learning plan for user_id 'user_without_plan' not found" in res.json()["detail"]


def test_get_progress_and_adaptation_endpoints():
    """20 to 25. Test GET endpoints for progress, skill progress, progress history, and adaptation history."""
    user_id = "test_endpoints_user"

    # Setup profile, gap analysis, plan, practice, submit
    client.post("/api/v1/profile", json={"user_id": user_id, "target_role": "AI/ML Engineer", "career_goal": "Goal"})
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    client.post(f"/api/v1/plans/generate?user_id={user_id}")
    gen_prac = client.post("/api/v1/practice/generate", json={"user_id": user_id, "task_id": "t1", "skill_name": "Statistics"})
    prac_id = gen_prac.json()["practice_id"]
    client.post(f"/api/v1/practice/{prac_id}/submit", json={"user_id": user_id, "answers": []})

    # Trigger adaptation
    res_adapt = client.post("/api/v1/adaptation/analyze", json={"user_id": user_id, "skill_name": "Statistics"})
    assert res_adapt.status_code == 200

    # Test GET /api/v1/progress
    res_prog = client.get(f"/api/v1/progress?user_id={user_id}")
    assert res_prog.status_code == 200

    # Test GET /api/v1/progress/skills
    res_skills = client.get(f"/api/v1/progress/skills?user_id={user_id}")
    assert res_skills.status_code == 200

    # Test GET /api/v1/progress/history
    res_hist = client.get(f"/api/v1/progress/history?user_id={user_id}")
    assert res_hist.status_code == 200

    # Test GET /api/v1/adaptation/history
    res_adapt_hist = client.get(f"/api/v1/adaptation/history?user_id={user_id}")
    assert res_adapt_hist.status_code == 200
    assert len(res_adapt_hist.json()) >= 1


def test_mongodb_failure_returns_503_for_progress_and_adaptation():
    """26. Test that DB offline state returns HTTP 503 Service Unavailable."""
    db_manager.db = None
    db_manager.client = None

    assert client.get("/api/v1/progress?user_id=u1").status_code == 503
    assert client.get("/api/v1/progress/skills?user_id=u1").status_code == 503
    assert client.get("/api/v1/adaptation/history?user_id=u1").status_code == 503
    assert client.post("/api/v1/adaptation/analyze", json={"user_id": "u1"}).status_code == 503


def test_end_to_end_adaptive_learning_loop_negative():
    """
    27. End-to-End Adaptive Loop (Negative / Low Score case):
    1. Learner creates profile & generates plan v1.
    2. Learner completes practice for Statistics and gets a LOW score (0%).
    3. EduPath detects progress status as 'struggling'.
    4. Adaptation Agent analyzes performance, decides action is 'review'.
    5. Plan version increments from v1 -> v2.
    6. A new review step is prepended to the Statistics module.
    7. Adaptation event is persisted in MongoDB.
    """
    user_id = "e2e_adaptive_loop_user_low"

    # Step 1: Create profile, gaps, and initial plan v1
    client.post("/api/v1/profile", json={"user_id": user_id, "target_role": "AI/ML Engineer", "career_goal": "Goal"})
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    plan_v1_res = client.post(f"/api/v1/plans/generate?user_id={user_id}")
    plan_v1 = plan_v1_res.json()
    assert plan_v1["version"] == 1

    # Step 2: Practice & Submit 0% score (Low score)
    gen_prac = client.post("/api/v1/practice/generate", json={"user_id": user_id, "task_id": "t1", "skill_name": "Statistics"})
    prac_id = gen_prac.json()["practice_id"]
    client.post(f"/api/v1/practice/{prac_id}/submit", json={"user_id": user_id, "answers": [{"question_id": "q1", "learner_answer": "Wrong Answer"}]})

    # Step 3: Trigger Adaptation
    adapt_res = client.post("/api/v1/adaptation/analyze", json={"user_id": user_id, "skill_name": "Statistics"})
    assert adapt_res.status_code == 200
    decision = adapt_res.json()

    assert decision["previous_status"] == "struggling"
    assert decision["action"] == "review"
    assert decision["affected_plan_version"] == 1
    assert decision["new_plan_version"] == 2

    # Step 4: Confirm plan version updated to v2 and review task was added
    plan_v2_res = client.get(f"/api/v1/plans?user_id={user_id}")
    plan_v2 = plan_v2_res.json()
    assert plan_v2["version"] == 2

    stat_module = [m for m in plan_v2["modules"] if m["skill_name"] == "Statistics"][0]
    first_task_title = stat_module["tasks"][0]["title"]
    assert "Review" in first_task_title


def test_end_to_end_adaptive_learning_loop_positive():
    """
    28. End-to-End Adaptive Loop (Positive / High Score case):
    1. Learner completes practice for Python and gets HIGH score (100%).
    2. EduPath detects progress status as 'strong'.
    3. Adaptation Agent decides action is 'move_forward'.
    4. Roadmap advances without adding redundant review tasks.
    """
    user_id = "e2e_adaptive_loop_user_high"

    client.post("/api/v1/profile", json={"user_id": user_id, "target_role": "Backend Developer", "career_goal": "Goal"})
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    client.post(f"/api/v1/plans/generate?user_id={user_id}")

    # Generate practice & submit 100% correct answers for all questions
    gen_prac = client.post("/api/v1/practice/generate", json={"user_id": user_id, "task_id": "t1", "skill_name": "Python"})
    prac_session = gen_prac.json()
    py_answers = {
        "q_py_101": "Tuple",
        "q_py_102": "try / except",
        "q_py_103": "len()",
        "q_py_104": "def",
        "q_py_105": "False",
        "q_py_106": "math",
        "q_py_107": "{}",
        "q_py_108": "//",
        "q_py_109": "for",
        "q_py_110": "import json",
    }
    answers = []
    for q in prac_session["questions"]:
        qid = q["question_id"]
        ans = py_answers.get(qid) or (q["options"][0] if q.get("options") else "Tuple")
        answers.append({"question_id": qid, "learner_answer": ans})

    client.post(f"/api/v1/practice/{prac_session['practice_id']}/submit", json={"user_id": user_id, "answers": answers})

    # Trigger Adaptation
    adapt_res = client.post("/api/v1/adaptation/analyze", json={"user_id": user_id, "skill_name": "Python"})
    assert adapt_res.status_code == 200
    decision = adapt_res.json()

    assert decision["previous_status"] == "strong"
    assert decision["action"] == "move_forward"
