# End-to-End EduPath User Journey (Task 2.1)

## Overview
EduPath connects 5 specialized autonomous AI agents into a seamless, human-centric career learning journey:

1. **Start Journey**: Learner clicks "Build My Learning Path" on the approved homepage and navigates to `/onboarding`.
2. **Create Learner Profile**: Learner submits their background, education, current skills, and target role (`AI/ML Engineer`, `Backend Developer`, `Frontend Developer`, `Data Scientist`).
3. **Profile Analysis**: Profile Agent ingests data, normalizes skill names, computes evidence-backed confidence scores, and stores the profile in MongoDB.
4. **Skill Gap Analysis**: Skill Gap Agent evaluates candidate capabilities against benchmark role requirements, identifying `strong`, `meets_requirement`, `needs_improvement`, and `missing` competencies.
5. **Learning Path Generation**: Learning Planner Agent constructs a prerequisite-ordered, weekly-chunked roadmap ($v1$).
6. **Current Learning Task**: Dashboard & Learning view highlight "YOUR NEXT STEP" with skill details, estimated duration, and justification.
7. **Resource Discovery**: Resource Agent recommends curated documentation and video materials for the current topic.
8. **Practice Session**: Practice Agent generates a structured quiz (`mcq`, `short_answer`).
9. **Submission & Scoring**: Practice Agent evaluates answers, calculates percentage score, and returns detailed per-question explanations.
10. **Progress Measurement**: Progress Agent categorizes score into performance status (`strong`, `on_track`, `needs_review`, `struggling`) and trend.
11. **Path Recalibration & Adaptation**: Adaptation Agent modifies the learning plan, prepends review or practice tasks, increments plan version ($v1 \rightarrow v2$), and sets a new next step.

---

## Brand Theme & Design System
- Primary Accent: `#FF9F43` (Orange)
- Secondary Accent: `#87CEEB` (Sky Blue)
- Background Surface: `#FFF8F0` / Dark Background `#25252A`
- Clean, uncluttered UI with 1 dominant action per screen.
