# CODE DOCTOR — ACADEMIC PROJECT REPORT

## 1. ABSTRACT
Code Doctor is a platform-independent intelligent coding diagnosis, prediction, repair, verification, and developer learning ecosystem. Unlike traditional IDE-locked linters, Code Doctor decouples the central diagnostic engine from specific client interfaces, providing a universal service layer accessible via Web Dashboard, REST API, CLI, and IDE extensions.

## 2. INTRODUCTION
Modern software engineering requires rapid debugging and continuous quality assurance. Existing error diagnostic tools suffer from vendor lock-in, fragmented error formats, and lack of root cause resolution. Code Doctor addresses these challenges by introducing a Universal Error Model and automated Code Surgery engine.

## 3. PROBLEM STATEMENT

Developers spend significant time parsing verbose stack traces, identifying downstream consequences, and manually crafting fixes. Existing static analysis tools output disconnected warnings without offering verified automated repairs or developer learning insights.

## 4. EXISTING SYSTEM
Conventional systems often rely on standalone linters and language-specific analysis tools that produce warnings in different formats and may require separate integrations.

## 5. LIMITATIONS OF EXISTING SYSTEM
1. Vendor lock-in to single IDE environments.
2. Inconsistent error taxonomy across languages.
3. Lack of cascading root cause analysis.
4. Blind code replacements without safe fix verification.
5. No long-term developer Error DNA tracking.

## 6. PROPOSED SYSTEM
Code Doctor introduces a centralized engine architecture that normalizes all programming errors into a Universal Error Model. It features predictive static analysis, safe fix verification, transparent Code Health Scoring, multi-level learning modes, and multi-platform adapters.

## 7. OBJECTIVES
1. Build a reusable platform-independent Code Doctor Engine.
2. Normalize language errors into standard diagnostic categories.
3. Perform cascading root cause resolution.
4. Provide automated Code Surgery repair with diff previews.
5. Safely verify generated fixes before applying.
6. Calculate transparent Code Health Scores (0-100).
7. Track developer Error DNA profiles.

## 8. SCOPE
Version 1.0 implements full core engine functionality, Python AST and JavaScript static analyzers, FastAPI REST API, React Web Dashboard, Python CLI (`codedoctor`), VS Code extension adapter, and GitHub Actions CI/CD pipeline integration.

## 9. SYSTEM REQUIREMENTS
* **Backend**: Python 3.12+, FastAPI, SQLAlchemy, Pydantic, Pytest
* **Frontend**: React 18, TypeScript, Vite, CSS, Lucide Icons
* **CLI**: Python Click/Argparse with Rich terminal formatting
* **Database**: SQLite (local) / PostgreSQL (production)

## 10. FUNCTIONAL REQUIREMENTS
* FR-1: Accept source code and project directories for scanning.
* FR-2: Normalize diagnostic items into Universal Error Model.
* FR-3: Identify primary root causes among cascading errors.
* FR-4: Generate minimal patch diffs and preview fixes.
* FR-5: Execute safe static verification on generated patches.
* FR-6: Compute weighted Code Health Score.
* FR-7: Track Error DNA and learning metrics over time.

## 11. NON-FUNCTIONAL REQUIREMENTS
* NFR-1: Performance — Designed for fast single-file analysis suitable for interactive developer workflows.
* NFR-2: Security — Zero arbitrary untrusted code execution on host.
* NFR-3: Privacy — Automatic secret redaction prior to AI calls.
* NFR-4: Usability — Responsive glassmorphic developer dashboard.

## 12. SYSTEM ARCHITECTURE
```
[Client Adapters: Web / CLI / VS Code / CI-CD]
                     │
                     ▼
         [FastAPI REST API /api/v1]
                     │
                     ▼
       [Code Doctor Core Engine]
     ┌───────────────┴───────────────┐
     ▼                               ▼
[Pluggable Analyzers]     [Universal Error Model]
     │                               │
     └───────────────► [Root Cause Engine]
                             │
                             ▼
                    [Predictive Engine]
                             │
                             ▼
                   [Code Surgery Engine]
                             │
                             ▼
                 [Fix Verification Engine]
                             │
                             ▼
                   [Health Score Engine]
                             │
                             ▼
                    [Error DNA Engine]
```

## 13. MODULE DESCRIPTION
1. `CodeDoctorEngine`: Core orchestrator.
2. `PythonAnalyzer` & `JavaScriptAnalyzer`: AST & static rule analyzers.
3. `RootCauseAnalyzer`: Graph dependency resolution for cascading errors.
4. `PredictiveAnalysisEngine`: Hazard detection before runtime execution.
5. `CodeSurgeryEngine`: Patch diff generation using difflib.
6. `FixVerificationEngine`: Safe static re-parsing & rule clean checking.
7. `HealthScoreEngine`: Weighted category score calculation.
8. `ErrorDnaEngine`: Learning analytics generator.

## 14. DATABASE DESIGN
Relational schema containing `users`, `projects`, `file_scans`, `diagnoses`, and `health_reports`, with SQLAlchemy ORM models supporting scan history and diagnostic persistence.

## 15. API DESIGN
RESTful API with OpenAPI documentation at `/api/v1`:
* `POST /api/v1/analyze`
* `POST /api/v1/fix`
* `POST /api/v1/verify`
* `POST /api/v1/project/scan`
* `GET /api/v1/health-score`
* `GET /api/v1/error-dna`

## 16. ALGORITHMS
* **Root Cause Identification**: Topological sort and line-ordered AST evaluation.
* **Predictive Bounds Analysis**: Constant list length evaluation vs subscript constants.
* **Code Surgery Patching**: Unified diff algorithm (`difflib.unified_diff`).

## 17. IMPLEMENTATION
Implemented using Python 3.14, FastAPI, SQLAlchemy, React, TypeScript, Vite, CSS, and Lucide Icons.

## 18. TESTING
The system was tested through API integration tests and targeted functional tests covering diagnosis, predictive analysis, project scanning, code repair, fix verification, authentication, health scoring, and Error DNA.

## 19. RESULTS
* Python Syntax Error Detection: Successfully validated through targeted syntax-error testing.
* Predictive IndexError Bounds Detection: Successfully validated through targeted out-of-bounds access testing.
* Code Surgery Verification: Zero syntax regressions on verified patches.

## 20. SECURITY
* Input sanitization & path traversal protection (`is_safe_path`).
* Secret scrubbing (`SensitiveDataRedactor`).
* Host execution isolation.

## 21. LIMITATIONS
* C++ and Java analyzers use regex pattern fallback in V1.
* Untrusted sandboxed code execution disabled on host machines for safety.

## 22. FUTURE ENHANCEMENTS
1. Full AST parsing for C++, Java, and Rust.
2. JetBrains, Visual Studio, and Jupyter plugin releases.
3. Docker containerized sandbox execution for runtime verification.

## 23. CONCLUSION
Code Doctor successfully demonstrates a universal, platform-independent coding diagnosis and repair ecosystem that empowers developers across IDEs, CLI, and Web.

## 24. REFERENCES

1. Python Software Foundation, "Python 3 Documentation — ast: Abstract Syntax Trees", Python Documentation, 2026.

2. FastAPI, "FastAPI Documentation", FastAPI Framework Documentation, 2026.

3. SQLAlchemy, "SQLAlchemy Documentation", SQLAlchemy Documentation, 2026.

4. React, "React Documentation", React Web Library Documentation, 2026.

5. Vite, "Vite Documentation", Vite Build Tool Documentation, 2026.

6. Python Software Foundation, "difflib — Helpers for computing deltas", Python Standard Library Documentation, 2026.