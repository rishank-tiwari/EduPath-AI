"""
Prerequisite & Skill Dependency Graph Service for EduPath.

Provides skill prerequisite resolution, dependency graph checking, and topological ordering.
"""

from typing import Dict, List, Set
from app.utils.logger import logger
from app.utils.skill_normalizer import normalize_skill_name


class PrerequisiteService:
    """Manages skill dependencies and prerequisite graphs across technical domains."""

    def __init__(self):
        # Default dependency graph: Map[Normalized Skill Name, List[Normalized Prerequisite Names]]
        self._prerequisites: Dict[str, List[str]] = {
            "Data Processing": ["Python"],
            "Probability": ["Python"],
            "Statistics": ["Probability"],
            "Machine Learning": ["Python", "Statistics", "Data Processing"],
            "Model Evaluation": ["Machine Learning"],
            "Deep Learning": ["Machine Learning"],
            "Model Deployment": ["Python", "Machine Learning"],
            "MLOps": ["Machine Learning", "Model Deployment"],
            "Data Structures": ["Python"],
            "Algorithms": ["Data Structures"],
            "SQL": ["Python"],
            "Databases / SQL": ["Python"],
            "FastAPI / REST APIs": ["Python"],
            "System Design": ["FastAPI / REST APIs", "SQL"],
        }

    def get_prerequisites(self, skill_name: str) -> List[str]:
        """Returns normalized direct prerequisite skill names for a given skill."""
        norm_name = normalize_skill_name(skill_name)
        return self._prerequisites.get(norm_name, [])

    def order_by_prerequisites(self, skill_names: List[str]) -> List[str]:
        """
        Orders a list of skill names topologically based on prerequisite dependencies.
        Ensures prerequisite skills always precede dependent skills.
        """
        normalized_input = [normalize_skill_name(s) for s in skill_names]
        input_set = set(normalized_input)

        # Build in-degree map and adjacency list limited to the provided skills
        in_degree: Dict[str, int] = {s: 0 for s in normalized_input}
        adj: Dict[str, List[str]] = {s: [] for s in normalized_input}

        for skill in normalized_input:
            prereqs = self.get_prerequisites(skill)
            for prereq in prereqs:
                if prereq in input_set and prereq != skill:
                    adj[prereq].append(skill)
                    in_degree[skill] += 1

        # Kahn's Algorithm for Topological Sort
        queue = [s for s in normalized_input if in_degree[s] == 0]
        ordered: List[str] = []

        while queue:
            # Sort queue to preserve original relative order for independent nodes
            curr = queue.pop(0)
            ordered.append(curr)

            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Append any remaining skills in case of circular dependency (safety fallback)
        for s in normalized_input:
            if s not in ordered:
                ordered.append(s)

        return ordered

    def check_prerequisites_satisfied(
        self, skill_name: str, satisfied_skills: Set[str]
    ) -> bool:
        """
        Checks whether all direct prerequisites for a skill are in the satisfied set.
        """
        prereqs = self.get_prerequisites(skill_name)
        norm_satisfied = {normalize_skill_name(s) for s in satisfied_skills}
        return all(p in norm_satisfied for p in prereqs)


prerequisite_service = PrerequisiteService()
