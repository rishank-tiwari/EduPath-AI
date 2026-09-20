"""
Curated Foundational Resource Catalog for EduPath.

Provides verified, authoritative documentation, video, and tutorial resources across core domains.
"""

from typing import List
from app.schemas.resource import LearningResource
from app.utils.skill_normalizer import normalize_skill_name

# Curated catalog of authoritative learning resources
FOUNDATIONAL_RESOURCES: List[LearningResource] = [
    # Python
    LearningResource(
        resource_id="res_py_01",
        title="Python Official Tutorial",
        description="Official Python language documentation covering data structures, control flow, and modules.",
        resource_type="documentation",
        url="https://docs.python.org/3/tutorial/",
        skill_name="Python",
        difficulty="beginner",
        estimated_minutes=30,
        source="Python Software Foundation",
    ),
    LearningResource(
        resource_id="res_py_02",
        title="Python Data Structures In-Depth",
        description="Comprehensive guide to lists, dictionaries, sets, and tuple optimization in Python.",
        resource_type="tutorial",
        url="https://docs.python.org/3/tutorial/datastructures.html",
        skill_name="Python",
        difficulty="intermediate",
        estimated_minutes=45,
        source="Python Software Foundation",
    ),

    # Probability & Statistics
    LearningResource(
        resource_id="res_stat_01",
        title="Khan Academy — Probability & Statistics",
        description="Interactive video lectures covering random variables, probability distributions, and hypothesis testing.",
        resource_type="video",
        url="https://www.khanacademy.org/math/statistics-probability",
        skill_name="Statistics",
        difficulty="beginner",
        estimated_minutes=35,
        source="Khan Academy",
    ),
    LearningResource(
        resource_id="res_prob_01",
        title="Introduction to Probability Distributions",
        description="Comprehensive article explaining discrete vs continuous distributions, variance, and standard deviation.",
        resource_type="article",
        url="https://www.khanacademy.org/math/statistics-probability/random-variables-stats-library",
        skill_name="Probability",
        difficulty="beginner",
        estimated_minutes=25,
        source="Khan Academy",
    ),

    # Machine Learning
    LearningResource(
        resource_id="res_ml_01",
        title="Scikit-Learn Machine Learning User Guide",
        description="Authoritative reference for supervised learning, regression, classification, and model selection.",
        resource_type="documentation",
        url="https://scikit-learn.org/stable/user_guide.html",
        skill_name="Machine Learning",
        difficulty="intermediate",
        estimated_minutes=40,
        source="Scikit-Learn",
    ),

    # Deep Learning & PyTorch
    LearningResource(
        resource_id="res_dl_01",
        title="PyTorch Deep Learning 60-Minute Blitz",
        description="Hands-on tutorial building neural networks, loss functions, and autograd tensor operations in PyTorch.",
        resource_type="tutorial",
        url="https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
        skill_name="Deep Learning",
        difficulty="intermediate",
        estimated_minutes=60,
        source="PyTorch Foundation",
    ),

    # FastAPI & Web APIs
    LearningResource(
        resource_id="res_fastapi_01",
        title="FastAPI Official First Steps",
        description="Official guide to constructing high-performance REST APIs with Python and Pydantic validation.",
        resource_type="documentation",
        url="https://fastapi.tiangolo.com/tutorial/first-steps/",
        skill_name="FastAPI / REST APIs",
        difficulty="beginner",
        estimated_minutes=30,
        source="FastAPI Official Docs",
    ),

    # SQL & Databases
    LearningResource(
        resource_id="res_sql_01",
        title="SQLite SQL Tutorial & Query Guide",
        description="Learn SELECT statements, JOIN operations, aggregations, and database indexing fundamentals.",
        resource_type="documentation",
        url="https://sqlite.org/docs.html",
        skill_name="SQL",
        difficulty="beginner",
        estimated_minutes=30,
        source="SQLite Documentation",
    ),

    # MLOps & Model Deployment
    LearningResource(
        resource_id="res_mlops_01",
        title="MLOps Architecture & Model Serving Overview",
        description="Introduction to continuous integration, model registries, containerization, and monitoring.",
        resource_type="article",
        url="https://scikit-learn.org/stable/modules/model_persistence.html",
        skill_name="MLOps",
        difficulty="intermediate",
        estimated_minutes=35,
        source="Scikit-Learn / MLOps Guide",
    ),
]


def get_curated_resources(skill_name: str, difficulty: str = "beginner") -> List[LearningResource]:
    """
    Returns matching curated learning resources for a given skill and difficulty.
    Falls back to matching by normalized skill name across difficulties if exact match is scarce.
    """
    norm_skill = normalize_skill_name(skill_name)
    norm_diff = difficulty.lower()

    # Exact skill match
    matches = [
        r for r in FOUNDATIONAL_RESOURCES
        if normalize_skill_name(r.skill_name) == norm_skill
    ]

    if not matches:
        # Generic fallback resource if skill is not directly in curated dataset
        return [
            LearningResource(
                resource_id=f"res_gen_{norm_skill[:6]}",
                title=f"Official {skill_name} Technical Reference",
                description=f"Curated foundational study guide and documentation for {skill_name}.",
                resource_type="documentation",
                url="[Configured Resource Documentation Placeholder]",
                skill_name=skill_name,
                difficulty=difficulty,
                estimated_minutes=30,
                source="EduPath Learning Engine",
            )
        ]

    # Sort so matching difficulty comes first
    matches.sort(key=lambda r: 0 if r.difficulty == norm_diff else 1)
    return matches
