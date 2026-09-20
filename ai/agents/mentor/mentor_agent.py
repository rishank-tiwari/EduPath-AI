"""
Context-Aware AI Mentor Agent Implementation for EduPath (PHASE 2 TASK 2.2).

Consumes sanitized learner context (profile, skill gaps, learning plan, current task, practice, progress, adaptation)
and responds naturally to learner inquiries using provider abstraction or deterministic fallback.
"""

from datetime import datetime
import logging
import re
import uuid
from typing import Any, Dict, Optional
from ai.agents.base_agent import AgentTrace, BaseAgent
from ai.agents.mentor.context_builder import MentorContextBuilder
from ai.providers.factory import UnimplementedAIProvider, get_ai_provider
from app.schemas.mentor import MentorResponse, SanitizedMentorContext

logger = logging.getLogger("edupath.mentor_agent")


class MentorAgent(BaseAgent):
    """
    Context-Aware AI Mentor Agent.
    Answers questions using the learner's actual EduPath journey state.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="MentorAgent",
            description="Provides context-aware guidance, explanations, and advice tailored to the learner's EduPath state.",
            provider=provider or get_ai_provider(),
        )

    async def execute(self, inputs: Dict[str, Any]) -> MentorResponse:
        """
        Executes Mentor Agent request.
        Expects inputs to contain `user_id` and `message`.
        """
        trace_id = f"tr_{uuid.uuid4().hex[:10]}"
        start_time = datetime.utcnow()

        user_id = inputs.get("user_id", "demo_user_1")
        message = inputs.get("message", "").strip()

        # 1. Build real sanitized learner context from DB repositories
        context = MentorContextBuilder.build_context(user_id)

        # 2. Determine response strategy: LLM vs Fallback
        use_fallback = isinstance(self.provider, UnimplementedAIProvider) or not getattr(self.provider, "api_key", None)

        if not use_fallback:
            try:
                response_obj = await self._generate_llm_response(message, context)
            except Exception as err:
                logger.warning(f"LLM generation failed ({str(err)}). Falling back to deterministic context handler.")
                response_obj = self._generate_fallback_response(message, context)
        else:
            response_obj = self._generate_fallback_response(message, context)

        # 3. Emit execution trace
        self._last_trace = AgentTrace(
            trace_id=trace_id,
            agent_name=self.name,
            input_data={"user_id": user_id, "message": message},
            decision=f"Generated {response_obj.response_mode} response for topic '{response_obj.context_topic}'.",
            tools_used=["mentor_context_builder"],
            output_data={
                "context_topic": response_obj.context_topic,
                "response_mode": response_obj.response_mode,
                "suggested_action": response_obj.suggested_action,
            },
            status="success",
            created_at=start_time,
        )

        return response_obj

    async def _generate_llm_response(self, message: str, context: SanitizedMentorContext) -> MentorResponse:
        """Generates mentor completion using configured LLM provider."""
        system_prompt = (
            "You are EduPath AI Mentor, a friendly, context-aware learning companion. "
            "Use ONLY the provided learner context. Do NOT invent or hallucinate skills, scores, tasks, or roles. "
            "Speak naturally in clear, encouraging language. Never use internal AI agent jargon."
        )

        task_str = f"{context.current_learning_task['title']} ({context.current_learning_task.get('skill_name', 'General')})" if context.current_learning_task else "None"

        practice_str = "No practice recorded yet"
        if context.recent_practice_result:
            pr = context.recent_practice_result
            practice_str = f"{pr.get('percentage', 0)}% score in {pr.get('topic', 'Practice')} ({pr.get('skill_name', 'Skill')})"

        adaptation_str = "No adaptation events recorded yet"
        if context.recent_adaptation:
            ra = context.recent_adaptation
            adaptation_str = f"Plan updated to v{ra.get('new_plan_version', 2)} because: {ra.get('reason', 'performance assessment')}"

        evidence_str = "No document/resume evidence recorded yet"
        if context.document_evidence:
            ev_list = [f"{ev.get('skill_name')}: {ev.get('description')}" for ev in context.document_evidence if isinstance(ev, dict)]
            if ev_list:
                evidence_str = "; ".join(ev_list)

        context_prompt = (
            f"LEARNER CONTEXT:\n"
            f"- User ID: {context.user_id}\n"
            f"- Target Role: {context.target_role}\n"
            f"- Current Skills: {', '.join(context.current_skills) if context.current_skills else 'None declared'}\n"
            f"- Skill Gaps to Improve: {', '.join(context.skills_to_improve) if context.skills_to_improve else 'None'}\n"
            f"- Missing Skills: {', '.join(context.missing_skills) if context.missing_skills else 'None'}\n"
            f"- Resume / Document Evidence: {evidence_str}\n"
            f"- Current Learning Task: {task_str}\n"
            f"- Recent Practice Result: {practice_str}\n"
            f"- Recent Adaptation History: {adaptation_str}\n\n"
            f"LEARNER QUESTION:\n{message}\n"
        )

        raw_text = await self.provider.generate(prompt=context_prompt, system_prompt=system_prompt)
        topic = context.current_learning_task["skill_name"] if context.current_learning_task else "Learning Path"
        suggested_action = context.current_learning_task["title"] if context.current_learning_task else None

        mode_label = "llm"

        return MentorResponse(
            response=raw_text.strip(),
            context_topic=topic,
            suggested_action=suggested_action,
            response_mode=mode_label,
            related_skill=topic,
            related_task=suggested_action,
            related_gap=context.missing_skills[0] if context.missing_skills else None,
        )

    def _generate_fallback_response(self, message: str, context: SanitizedMentorContext) -> MentorResponse:
        """
        Context-aware, deterministic fallback response engine.
        Answers all 8 core prompt categories using actual context fields.
        """
        msg_lower = message.lower()
        target_role = context.target_role or "AI/ML Engineer"

        # Determine primary skill & task context
        task_info = context.current_learning_task or {}
        task_title = task_info.get("title", "Core Foundations")
        skill_name = task_info.get("skill_name") or (context.missing_skills[0] if context.missing_skills else "Statistics")

        related_gap = context.missing_skills[0] if context.missing_skills else (context.skills_to_improve[0] if context.skills_to_improve else None)

        # Intent 1: Next step / What to learn next
        if any(w in msg_lower for w in ["next", "should i learn", "what's next"]):
            plan_ver = context.learning_plan_summary.get("version", 1) if context.learning_plan_summary else 1
            if context.current_learning_task:
                resp_text = (
                    f"Your next step is '{task_title}' ({task_info.get('estimated_minutes', 30)} min). "
                    f"In this task, you'll focus on {skill_name} to continue progressing along your learning path (v{plan_ver})."
                )
                suggested_action = task_title
            else:
                resp_text = f"Your next step is to start your onboarding roadmap for your target role of {target_role}."
                suggested_action = "Start Learning Path"

            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=suggested_action,
                response_mode="fallback",
                related_skill=skill_name,
                related_task=suggested_action,
                related_gap=related_gap,
            )

        # Intent 2: Why learning / Skill gap inquiry
        if any(w in msg_lower for w in ["why am i learning", "why do i need", "why statistics", "why mlops"]):
            if skill_name in context.missing_skills:
                gap_reason = f"it is currently identified as a missing skill for {target_role}."
            elif skill_name in context.skills_to_improve:
                gap_reason = f"it is an area identified for improvement to meet {target_role} standards."
            else:
                gap_reason = f"it forms a foundational component for your {target_role} career goal."

            resp_text = (
                f"You're learning {skill_name} because {gap_reason} "
                f"Mastering this will help bridge your profile gaps and build your confidence."
            )
            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=f"Start {skill_name} Practice",
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=skill_name,
            )

        # Intent 3: Progress / Why did plan change
        if any(w in msg_lower for w in ["plan change", "learning path change", "adaptation", "changed"]):
            if context.recent_adaptation:
                reason = context.recent_adaptation.get("reason", "your recent practice performance.")
                new_ver = context.recent_adaptation.get("new_plan_version", 2)
                resp_text = f"Your learning path was updated (v{new_ver}) because {reason}"
            else:
                plan_ver = context.learning_plan_summary.get("version", 1) if context.learning_plan_summary else 1
                resp_text = f"Your learning path is currently on version v{plan_ver}, structured to guide you step-by-step toward becoming a {target_role}."

            return MentorResponse(
                response=resp_text,
                context_topic="Learning Path Adaptation",
                suggested_action=task_title,
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=related_gap,
            )

        # Intent 4: Mistake explanation / Practice feedback
        if any(w in msg_lower for w in ["wrong", "mistake", "score", "practice result"]):
            if context.recent_practice_result:
                pr = context.recent_practice_result
                resp_text = (
                    f"In your recent practice on {pr.get('topic', skill_name)}, you scored {pr.get('score')}/{pr.get('total_questions')} "
                    f"({pr.get('percentage')}%). EduPath noticed you may need a bit more review in {pr.get('skill_name', skill_name)} "
                    f"to solidify your understanding before moving forward."
                )
            else:
                resp_text = "I don't have a recent practice result for that topic yet. Completing a practice session will let me give you specific feedback."

            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=f"Review {skill_name} Basics",
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=skill_name,
            )

        # Intent 5: Practice question request
        if any(w in msg_lower for w in ["practice question", "test me", "quiz"]):
            resp_text = (
                f"Here is a quick practice question for {skill_name}:\n\n"
                f"What is the main objective when fitting a probability distribution to sample data?\n"
                f"(A) To model the underlying data generation process and estimate likelihoods.\n"
                f"(B) To eliminate all variation in raw measurements."
            )
            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=f"Start Practice for {skill_name}",
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=related_gap,
            )

        # Intent 6: Example request
        if any(w in msg_lower for w in ["example", "sample"]):
            resp_text = (
                f"Here is a real-world example in {skill_name}:\n\n"
                f"Imagine predicting housing prices based on location and size. "
                f"The input variables (sq ft, bedrooms) are analyzed to estimate the output variable (price), "
                f"illustrating how core {skill_name} concepts apply in practical engineering."
            )
            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=f"Explore {skill_name} Resources",
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=related_gap,
            )

        # Intent 7: Explanation in simple words / General explanation
        if any(w in msg_lower for w in ["simple words", "explain", "what is"]):
            resp_text = (
                f"Here's a simple way to think about {skill_name}: "
                f"It provides foundational principles that allow AI models to analyze data, find patterns, and make accurate predictions. "
                f"For your {target_role} goal, mastering these core ideas ensures your systems are reliable."
            )
            return MentorResponse(
                response=resp_text,
                context_topic=skill_name,
                suggested_action=task_title,
                response_mode="fallback",
                related_skill=skill_name,
                related_task=task_title,
                related_gap=related_gap,
            )

        # Intent 8: Default context-aware response
        resp_text = (
            f"Hello! As your EduPath AI Mentor, I'm tracking your journey toward {target_role}. "
            f"Your current focus is '{task_title}' in {skill_name}. "
            f"How can I help you understand this concept or guide your next step?"
        )
        return MentorResponse(
            response=resp_text,
            context_topic=skill_name,
            suggested_action=task_title,
            response_mode="fallback",
            related_skill=skill_name,
            related_task=task_title,
            related_gap=related_gap,
        )
