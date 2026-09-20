# Mentor Agent — Context-Aware AI Learning Companion

## Overview
The **Mentor Agent** serves as a context-aware learning companion within EduPath. Rather than behaving like a generic chatbot, it constructs real-time context from the learner's live state (Profile, Target Role, Current Skills, Skill Gaps, Learning Plan, Current Task, Recent Practice Results, Progress Summary, and Recent Adaptation Events) to deliver personalized, grounded guidance.

---

## Agent Purpose & Responsibilities
1. **Receive Learner Question**: Process user messages from the AI Mentor interface.
2. **Build Learner Context**: Fetch and aggregate data across user repositories without hallucination or inventing missing facts.
3. **Classify Intent**: Identify the target context topic and response type (Explanation, Reason, Example, Practice, Next step, Mistake explanation, Progress explanation, Skill-gap explanation).
4. **Generate Contextual Guidance**: Utilize provider abstraction (or intelligent deterministic fallbacks when AI provider is unconfigured).
5. **Suggest Actionable Next Steps**: Provide concrete, plan-aligned next steps for the user.

---

## Inputs & Context Schema
The Context Builder (`ai.agents.mentor.context_builder.MentorContextBuilder`) aggregates:
- `target_role`: The user's target career path.
- `current_skills`: Verified user skill array.
- `skill_gaps`: Identified missing or weak skills.
- `current_learning_task`: The active item in the learning plan.
- `learning_plan`: Ordered roadmap of topics/modules.
- `recent_practice_result`: Most recent quiz/exercise score, weak areas, and breakdown.
- `progress_summary`: Total modules completed, overall score average, and completion rate.
- `recent_adaptation`: Latest adaptation trigger, cause, and plan modification history.

---

## Output Schema (`MentorResponse`)
```json
{
  "response": "Statistics is part of your learning path because it is currently a gap for your AI/ML Engineer goal.",
  "context_topic": "Statistics",
  "suggested_action": "Review Probability Basics",
  "response_mode": "fallback",
  "related_skill": "Statistics",
  "related_task": "Probability Basics",
  "related_gap": "Statistics & Probability",
  "created_at": "2026-09-20T13:40:00Z"
}
```

---

## Provider Abstraction & Fallback Behavior
The Mentor Agent uses `BaseAIProvider`. When an LLM provider (e.g. OpenAI, Claude, Gemini) is connected, it uses standard prompt generation. When unconfigured (`UnimplementedAIProvider`), the agent executes strict, deterministic fallback rules based directly on stored context data and sets `response_mode: "fallback"`. Fallback text is never disguised as a real LLM response.

---

## Hallucination Controls
- Only stored, actual learner data is referenced.
- If practice results or adaptation history do not exist for a given user, the agent explicitly states: *"I don't have a recent practice result for that topic yet."*
- Learning path recommendations strictly mirror the user's active plan items rather than fabricating arbitrary curricula.

---

## Supported Question Types
1. **Explanation**: *"Explain this in simple words."*
2. **Reason**: *"Why am I learning this?"*
3. **Example**: *"Give me an example."*
4. **Practice**: *"Give me a practice question."*
5. **Next Step**: *"What should I learn next?"*
6. **Mistake Explanation**: *"Why did I get this wrong?"*
7. **Progress Explanation**: *"Why did my learning path change?"*
8. **Skill-Gap Explanation**: *"Why do I need Statistics?"*
