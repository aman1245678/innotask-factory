"""
InnoTask Factory — Command Line Interface (CLI)
Provides commands to list, inspect, generate, and verify Harbor v0.25 task packages.
"""

import sys
import argparse
import json
from pathlib import Path
from core.verifier import HarborTaskVerifier

TASKS_DIR = Path("tasks")

def list_tasks():
    if not TASKS_DIR.exists():
        print("No tasks found.")
        return
    tasks = [d for d in TASKS_DIR.iterdir() if d.is_dir() and (d / "task.json").exists()]
    print(f"\n📦 Found {len(tasks)} Harbor v0.25 Task Packages:\n" + "=" * 55)
    for t in tasks:
        with open(t / "task.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            req = data.get("requirement", {})
            print(f"🔹 ID:         {data.get('task_id')}")
            print(f"   Title:      {req.get('title')}")
            print(f"   Difficulty: {req.get('difficulty')}")
            print(f"   Target:     {data.get('target_repo')}")
            print(f"   Files:      {', '.join(req.get('affected_files', []))}")
            print("-" * 55)

def verify_task(task_id: str):
    task_dir = TASKS_DIR / task_id
    if not task_dir.exists():
        print(f"❌ Error: Task '{task_id}' not found in {TASKS_DIR}")
        return
    print(f"\n🔍 Verifying Harbor Task: {task_id} ...")
    verifier = HarborTaskVerifier(task_dir)
    res = verifier.run_full_validation_suite()
    print("\n" + "=" * 55)
    print(f"Static Schema Check: {'✅ PASS' if res['static_schema_check']['passed'] else '❌ FAIL'}")
    print(f"No-Op Validation:    {'✅ PASS' if res['noop_validation']['passed'] else '❌ FAIL'}")
    print(f"Oracle Validation:   {'✅ PASS' if res['oracle_validation']['passed'] else '❌ FAIL'}")
    print(f"Regression Safety:   {'✅ PASS' if res['regression_safety']['passed'] else '❌ FAIL'}")
    print("=" * 55)
    print(f"🏆 Overall Harbor Score: {res['score']}/100\n")

def main():
    parser = argparse.ArgumentParser(description="InnoTask Factory — Harbor v0.25 Task Engineering CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all generated Harbor task packages")
    
    verify_p = subparsers.add_parser("verify", help="Run Harbor rubric validation on a task")
    verify_p.add_argument("task_id", help="ID of the task to verify")

    args = parser.parse_args()

    if args.command == "list":
        list_tasks()
    elif args.command == "verify":
        verify_task(args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
