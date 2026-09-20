"""
Skill Normalization Engine for EduPath.

Provides alias resolution to standardize raw learner skill declarations against benchmark names.
"""

from typing import Dict

# Dictionary mapping common raw/alias skill strings to canonical benchmark names
SKILL_ALIAS_MAP: Dict[str, str] = {
    "python programming": "Python",
    "python3": "Python",
    "py": "Python",
    "ml": "Machine Learning",
    "machine learning algorithms": "Machine Learning",
    "machine learning basics": "Machine Learning",
    "deep learning / neural networks": "Deep Learning",
    "neural networks": "Deep Learning",
    "dl": "Deep Learning",
    "pytorch": "Deep Learning",
    "stats": "Statistics",
    "statistical analysis": "Statistics",
    "probability & statistics": "Statistics",
    "mlops & deployment": "MLOps",
    "model serving": "Model Deployment",
    "deployment": "Model Deployment",
    "data preprocessing": "Data Processing",
    "data manipulation": "Data Processing",
    "pandas & numpy": "Data Processing",
}


def normalize_skill_name(raw_name: str) -> str:
    """
    Normalizes raw skill name string to canonical benchmark representation.
    Example: 'Python Programming' -> 'Python'
    """
    if not raw_name:
        return ""

    cleaned = raw_name.strip()
    lowered = cleaned.lower()

    if lowered in SKILL_ALIAS_MAP:
        return SKILL_ALIAS_MAP[lowered]

    # Return trimmed original name if no explicit alias exists
    return cleaned
