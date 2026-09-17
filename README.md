# CODE DOCTOR — Universal Intelligent Code Diagnosis & Repair Platform

> **Tagline**: *Diagnose. Repair. Verify. Improve.*

Code Doctor is a platform-independent intelligent coding diagnosis, prediction, repair, verification, and developer learning ecosystem. 

---

## Key Features

1. **Platform Independence**: Core diagnosis engine (`Code Doctor Core Engine`) is completely decoupled from VS Code or any specific IDE.
2. **Universal Error Model**: Standardized diagnostic schema categorizing errors into `SYNTAX`, `TYPE`, `LOGIC`, `RUNTIME`, `MEMORY`, `SECURITY`, `PERFORMANCE`, `STYLE`, `DEPENDENCY`, and `CONFIGURATION`.
3. **Cascading Root Cause Analysis**: Identifies primary root cause among dependent error chains (e.g. missing import causing undefined function causing runtime failure).
4. **Predictive Static Analysis**: Detects out-of-bounds array access, null pointer hazards, and infinite loops prior to runtime execution with confidence scores.
5. **Code Surgery & Fix Generator**: Generates minimal patch diffs and preview fixes without overwriting user files blindly.
6. **Safe Fix Verification Engine**: Safely re-evaluates syntax, AST structure, and rules before marking fixes as `VERIFIED`.
7. **Transparent Code Health Score**: Calculates overall health (0-100) using weighted sub-scores: Correctness (30%), Security (20%), Maintainability (20%), Performance (15%), Quality (15%).
8. **Developer Error DNA**: Tracks recurring error categories, improvement trends, and language weaknesses over time.
9. **Multi-Level Learning Mode**: Tailors diagnostic explanations to `Beginner`, `Intermediate`, and `Advanced` skill tiers.
10. **Offline-First Architecture**: Operates 100% offline using AST, Ruff, and Bandit rules, with optional Google Gemini AI enhancement.

---

## Technology Stack

* **Backend**: Python 3.12+, FastAPI, Pydantic, SQLAlchemy, SQLite/PostgreSQL, Pytest
* **Frontend**: React, TypeScript, Vite, CSS, Lucide Icons
* **CLI**: Python `codedoctor` CLI tool (`pip install -e cli/`)
* **Adapters**: REST API (`/api/v1`), VS Code Extension (`adapters/vscode`), GitHub Actions CI/CD (`.github/workflows/code-doctor.yml`)

---

## Quick Start Guide

### 1. Start FastAPI Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open API docs at `http://127.0.0.1:8000/docs`.

### 2. Run Backend Test Suite

```bash
cd backend
python -m pytest tests/
```

### 3. Run Python CLI (`codedoctor`)

```bash
python -m pip install -e cli/
codedoctor scan examples/python/cascading_errors.py
codedoctor scan examples/python/cascading_errors.py --format json
codedoctor fix examples/python/index_error.py
```

### 4. Start React Web Dashboard

```bash
cd frontend
npm install
npm run dev
```
Open Web Dashboard at `http://127.0.0.1:5173`.

