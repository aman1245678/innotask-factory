"""
InnoTask Factory — Comprehensive Automated Test Suite
Validates schema generation, Harbor v0.25 packaging, tri-phase verification rubrics,
and pallets/click task integrity.
"""

import unittest
from pathlib import Path
import json

from core.schema import HarborTaskPackage, TaskRequirement, HarborEnvironmentConfig
from core.extractor import FeatureExtractor
from core.task_packager import HarborTaskPackager
from core.verifier import HarborTaskVerifier

class TestInnoTaskFactory(unittest.TestCase):

    def setUp(self):
        self.output_dir = Path("test_tasks_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = FeatureExtractor("https://github.com/pallets/click", "7eb021a")
        self.packager = HarborTaskPackager(str(self.output_dir))

    def tearDown(self):
        import shutil
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_harbor_schema_generation(self):
        """Verify HarborTaskPackage serializes to compliant JSON with v0.25 spec."""
        task = self.extractor.generate_task_from_feature_spec(
            task_id="test_task_001",
            title="Test Feature",
            description="Test Description",
            acceptance_criteria=["Criterion 1"],
            affected_files=["src/test.py"],
            feature_test_code="def test_sample(): pass",
            reference_patch="--- a/test.py\n+++ b/test.py",
            difficulty="easy"
        )
        data = json.loads(task.to_json())
        self.assertEqual(data["harbor_spec_version"], "0.25.2")
        self.assertEqual(data["task_id"], "test_task_001")
        self.assertEqual(data["target_repo"], "https://github.com/pallets/click")

    def test_task_packaging_filesystem_compliance(self):
        """Verify packager creates all required Harbor files in isolated task folder."""
        task = self.extractor.generate_task_from_feature_spec(
            task_id="test_pack_001",
            title="Packaging Check",
            description="Verify files",
            acceptance_criteria=["Works"],
            affected_files=["src/click/core.py"],
            feature_test_code="def test_it(): assert True",
            reference_patch="diff --git a/file b/file\n",
            difficulty="easy"
        )
        task_dir = self.packager.package_task(task)

        expected_files = [
            "task.json",
            "instruction.md",
            "Dockerfile",
            "docker-compose.yaml",
            "solution.patch",
            "test_feature.py",
            "test.sh"
        ]
        for f in expected_files:
            self.assertTrue((task_dir / f).exists(), f"Missing Harbor required file: {f}")

    def test_tri_phase_verification_rubric(self):
        """Verify verifier executes static check, noop, oracle, and regression checks."""
        task = self.extractor.generate_task_from_feature_spec(
            task_id="test_rubric_001",
            title="Rubric Validation",
            description="Validation description",
            acceptance_criteria=["Check 1"],
            affected_files=["src/click/types.py"],
            feature_test_code="def test_code(): assert 1 == 1",
            reference_patch="valid patch content\n",
            difficulty="medium"
        )
        task_dir = self.packager.package_task(task)
        verifier = HarborTaskVerifier(task_dir)
        res = verifier.run_full_validation_suite()

        self.assertTrue(res["all_passed"])
        self.assertEqual(res["score"], 100)
        self.assertTrue(res["static_schema_check"]["passed"])
        self.assertTrue(res["noop_validation"]["passed"])
        self.assertTrue(res["oracle_validation"]["passed"])
        self.assertTrue(res["regression_safety"]["passed"])

    def test_pallets_click_live_tasks(self):
        """Verify the 2 generated tasks in tasks/ pass all Harbor checks."""
        tasks_dir = Path("tasks")
        click_tasks = ["task_click_001_deprecated_option", "task_click_002_case_insensitive_choice"]
        for t_id in click_tasks:
            t_path = tasks_dir / t_id
            self.assertTrue(t_path.exists(), f"Task {t_id} must exist in tasks/")
            verifier = HarborTaskVerifier(t_path)
            res = verifier.run_full_validation_suite()
            self.assertTrue(res["all_passed"], f"Task {t_id} failed rubric!")
            self.assertEqual(res["score"], 100)

if __name__ == "__main__":
    unittest.main()
