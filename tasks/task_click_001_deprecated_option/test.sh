#!/bin/bash
set -e

echo "=== Running Harbor v0.25 Task Verification for task_click_001_deprecated_option ==="

# Step 1: Run regression checks on existing baseline
echo "[1/2] Running regression tests..."
pytest tests/ -k "not test_feature" --tb=short || {
    echo "FAILED: Baseline regression checks broke!"
    exit 1
}

# Step 2: Run feature tests
echo "[2/2] Running feature requirement tests..."
pytest /test_feature.py -v || {
    echo "FAILED: Feature requirements not met!"
    exit 2
}

echo "SUCCESS: All Harbor verification checks passed!"
exit 0
