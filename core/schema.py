"""
InnoTask Factory — Harbor v0.25.x Standard Task Schema & Specification.
Defines data structures for task metadata, evaluation environments, and validation rubrics.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import json

@dataclass
class HarborEnvironmentConfig:
    docker_image: str = "python:3.11-slim"
    working_dir: str = "/workspace"
    setup_commands: List[str] = field(default_factory=lambda: [
        "pip install --upgrade pip",
        "pip install pytest build virtualenv",
        "pip install -e ."
    ])
    timeout_seconds: int = 300
    memory_limit: str = "2g"
    cpu_limit: str = "2"

@dataclass
class TaskRequirement:
    title: str
    description: str
    acceptance_criteria: List[str]
    affected_files: List[str]
    difficulty: str = "medium"  # easy, medium, hard
    category: str = "feature_development"

@dataclass
class HarborTaskPackage:
    task_id: str
    target_repo: str
    baseline_commit: str
    harbor_spec_version: str = "0.25.2"
    requirement: TaskRequirement = field(default_factory=lambda: TaskRequirement("", "", [], []))
    environment: HarborEnvironmentConfig = field(default_factory=HarborEnvironmentConfig)
    feature_tests: List[str] = field(default_factory=list)
    regression_tests: List[str] = field(default_factory=list)
    reference_patch: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
