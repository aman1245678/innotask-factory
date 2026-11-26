"""
InnoTask Factory — Harbor Task Packager
Builds containerized task packages conforming to Harbor v0.25 standardized architecture.
Outputs Dockerfile, docker-compose.yaml, instruction.md, test.sh, task.json, and solution.patch.
"""

import os
from pathlib import Path
from .schema import HarborTaskPackage

class HarborTaskPackager:
    """
    Serializes a HarborTaskPackage into the filesystem structure required by Harbor v0.25.x.
    """

    def __init__(self, output_root: str = "tasks"):
        self.output_root = Path(output_root)

    def package_task(self, task: HarborTaskPackage) -> Path:
        """
        Creates the standardized Harbor containerized directory.
        """
        task_dir = self.output_root / task.task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        # 1. task.json (Harbor standard metadata)
        with open(task_dir / "task.json", "w", encoding="utf-8") as f:
            f.write(task.to_json())

        # 2. instruction.md (Task prompt presented to the AI coding agent)
        instruction_content = f"""# Task: {task.requirement.title}

## Problem Description
{task.requirement.description}

## Acceptance Criteria
{"".join(f"- {criterion}\n" for criterion in task.requirement.acceptance_criteria)}

## Target Files
{"".join(f"- `{file}`\n" for file in task.requirement.affected_files)}

## Baseline Environment
- **Repository:** `{task.target_repo}`
- **Baseline Commit:** `{task.baseline_commit}`
- **Test Command:** `bash test.sh`
"""
        with open(task_dir / "instruction.md", "w", encoding="utf-8") as f:
            f.write(instruction_content)

        # 3. Dockerfile (Containerized reproducible environment)
        dockerfile_content = f"""# Harbor v0.25.x Standardized Task Container
FROM {task.environment.docker_image}

WORKDIR {task.environment.working_dir}

# System dependencies
RUN apt-get update && apt-get install -y git bash curl && rm -rf /var/lib/apt/lists/*

# Clone baseline repository
RUN git clone {task.target_repo} {task.environment.working_dir} && \\
    git checkout {task.baseline_commit}

# Environment setup
{"".join(f"RUN {cmd}\n" for cmd in task.environment.setup_commands)}

# Copy task verification harness
COPY test.sh /test.sh
COPY test_feature.py /test_feature.py
RUN chmod +x /test.sh

CMD ["/test.sh"]
"""
        with open(task_dir / "Dockerfile", "w", encoding="utf-8") as f:
            f.write(dockerfile_content)

        # 4. docker-compose.yaml
        compose_content = f"""version: '3.8'
services:
  harbor-evaluator:
    build: .
    container_name: harbor_{task.task_id}
    working_dir: {task.environment.working_dir}
    volumes:
      - .:/harbor_host
    environment:
      - HARBOR_TASK_ID={task.task_id}
      - HARBOR_SPEC_VERSION={task.harbor_spec_version}
"""
        with open(task_dir / "docker-compose.yaml", "w", encoding="utf-8") as f:
            f.write(compose_content)

        # 5. solution.patch (Reference Oracle Implementation)
        with open(task_dir / "solution.patch", "w", encoding="utf-8") as f:
            f.write(task.reference_patch)

        # 6. test_feature.py (Feature Verification Test)
        feature_test_str = task.feature_tests[0] if task.feature_tests else "# No feature tests"
        with open(task_dir / "test_feature.py", "w", encoding="utf-8") as f:
            f.write(feature_test_str)

        # 7. test.sh (Automated Test Execution Script)
        test_sh_content = f"""#!/bin/bash
set -e

echo "=== Running Harbor v0.25 Task Verification for {task.task_id} ==="

# Step 1: Run regression checks on existing baseline
echo "[1/2] Running regression tests..."
pytest tests/ -k "not test_feature" --tb=short || {{
    echo "FAILED: Baseline regression checks broke!"
    exit 1
}}

# Step 2: Run feature tests
echo "[2/2] Running feature requirement tests..."
pytest /test_feature.py -v || {{
    echo "FAILED: Feature requirements not met!"
    exit 2
}}

echo "SUCCESS: All Harbor verification checks passed!"
exit 0
"""
        with open(task_dir / "test.sh", "w", encoding="utf-8") as f:
            f.write(test_sh_content)

        return task_dir
