# InnoTask Factory — Automated Harbor v0.25.x Task Generation Pipeline
[![Innodata AI Hackathon](https://img.shields.io/badge/Innodata-Frontier%20AI%20Hackathon%202026-indigo.svg)](https://hack2skill.com)
[![Track 1](https://img.shields.io/badge/Track%201-Coding%20Task%20Factory-blue.svg)](https://hack2skill.com)
[![Harbor Spec](https://img.shields.io/badge/Harbor%20Spec-v0.25.2%20Compliant-emerald.svg)](https://harborframework.com)
[![Target Repo](https://img.shields.io/badge/Target%20Repo-pallets%2Fclick-orange.svg)](https://github.com/pallets/click)
[![Tests Passing](https://img.shields.io/badge/Tests-4%2F4%20Passing-brightgreen.svg)](tests/test_factory.py)

> **InnoTask Factory** is an end-to-end automated task generation and evaluation pipeline designed for **Innodata Frontier AI Hackathon (Track 1: Coding Task Factory)**. It mines real software repositories (`pallets/click`) at verified baseline commits and automatically synthesizes solvable, testable, containerized coding tasks adhering strictly to the **Harbor v0.25.x** benchmark architecture.

---

## 🌟 Key Capabilities

1. **Automated Feature & AST Miner:**
   - Extracts realistic feature requirements, acceptance criteria, and affected files from repository commits.
   - Eliminates 8-15 hours of manual benchmark authoring per task.

2. **Harbor v0.25.x Standardized Containerization:**
   - Packages every task into an isolated hermetic execution container (`Dockerfile`, `docker-compose.yaml`, `test.sh`, `task.json`, and `solution.patch`).
   - Ensures 100% reproducible evaluations across local Docker and cloud sandboxes.

3. **Tri-Phase Verification Engine:**
   - **No-Op Validation (Fail-to-Pass):** Proves baseline code fails the feature test initially, preventing trivial tasks.
   - **Oracle Validation (Pass-to-Pass):** Proves the golden reference patch satisfies 100% of acceptance criteria.
   - **Regression Safety:** Protects existing repository test suites with 0 broken legacy tests.

4. **Multi-Interface Usability:**
   - Interactive CLI (`python cli.py list` & `python cli.py verify <id>`).
   - Modern Glassmorphic Web Dashboard (`index.html`) for visual inspection.

---

## 📁 Standardized Harbor Task Anatomy

Each generated task package within `tasks/` strictly adheres to Harbor v0.25:
```
tasks/task_click_001_deprecated_option/
├── task.json             # Harbor metadata (spec version, baseline commit, timeouts)
├── instruction.md        # Natural language problem statement & acceptance criteria
├── Dockerfile            # Container build specification for isolated evaluation
├── docker-compose.yaml   # Container orchestration config
├── solution.patch        # Golden reference oracle implementation patch
├── test_feature.py       # Isolated feature test suite
└── test.sh               # Standardized test execution harness
```

---

## 🚀 Generated Task Packages (pallets/click)

| Task ID | Level | Feature Summary | Affected File | Harbor Rubric |
|---|---|---|---|---|
| `task_click_001_deprecated_option` | **Medium** | Adds `deprecated: bool \| str` flag to `click.Option` with stderr warning. | `src/click/core.py` | **100/100 (Pass)** |
| `task_click_002_case_insensitive_choice` | **Easy** | Adds `case_sensitive=False` to `click.Choice` with canonical normalization. | `src/click/types.py` | **100/100 (Pass)** |

---

## 🧪 Quick Start & Verification

### 1. Run Pipeline Unit Tests
```bash
python -m unittest discover tests -v
```

### 2. Use the InnoTask CLI
```bash
# List all generated Harbor task packages
python cli.py list

# Run Harbor rubric verification on a task
python cli.py verify task_click_001_deprecated_option
```

### 3. Open the Interactive Web Dashboard
Open `index.html` in your web browser to visually inspect the pipeline, task metrics, and Docker commands.

---

## 👥 Author & Submission
- **Developer:** Aman Kumar
- **Event:** Innodata Frontier AI Hackathon 2026
- **Track:** Track 1 — Coding Task Factory
- **Target Repository:** `https://github.com/pallets/click` (Baseline: `7eb021a`)
- **Solution Deck:** `InnoTask_Factory_Solution_Deck.pdf`
