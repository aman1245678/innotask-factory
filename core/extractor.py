"""
InnoTask Factory — Feature Extraction Engine
Reusable strategy to extract realistic feature-development tasks from git repositories
by analyzing pull requests, feature diffs, and AST modifications.
"""

from typing import Dict, Any, List
import re
from .schema import HarborTaskPackage, TaskRequirement, HarborEnvironmentConfig

class FeatureExtractor:
    """
    Extracts structured, solvable, testable coding challenges from target repositories.
    Conforms to Harbor v0.25 task generation interface.
    """

    def __init__(self, repo_url: str = "https://github.com/pallets/click", baseline_commit: str = "7eb021a"):
        self.repo_url = repo_url
        self.baseline_commit = baseline_commit

    def generate_task_from_feature_spec(
        self,
        task_id: str,
        title: str,
        description: str,
        acceptance_criteria: List[str],
        affected_files: List[str],
        feature_test_code: str,
        reference_patch: str,
        difficulty: str = "medium"
    ) -> HarborTaskPackage:
        """
        Creates a validated HarborTaskPackage ready for containerization.
        """
        requirement = TaskRequirement(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            affected_files=affected_files,
            difficulty=difficulty,
            category="feature_development"
        )

        task = HarborTaskPackage(
            task_id=task_id,
            target_repo=self.repo_url,
            baseline_commit=self.baseline_commit,
            harbor_spec_version="0.25.2",
            requirement=requirement,
            environment=HarborEnvironmentConfig(
                docker_image="python:3.11-slim",
                setup_commands=[
                    "pip install --upgrade pip",
                    "pip install pytest",
                    "pip install -e ."
                ]
            ),
            feature_tests=[feature_test_code],
            regression_tests=["pytest tests/test_basic.py"],
            reference_patch=reference_patch,
            metadata={
                "generator": "InnoTask-Factory-v1.0",
                "framework": "Harbor-v0.25.x",
                "target_project": "pallets/click"
            }
        )
        return task
