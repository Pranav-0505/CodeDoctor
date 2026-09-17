# Code Doctor System Architecture

```
USER / PLATFORM (Web / CLI / VS Code / CI-CD)
          │
          ▼
   PLATFORM ADAPTER
          │
          ▼
   CODE DOCTOR API (FastAPI /api/v1)
          │
          ▼
   CODE DOCTOR CORE ENGINE
   ┌──────────────────────────────┬──────────────────────────────┐
   │                              │                              │
   ▼                              ▼                              ▼
PLUGGABLE ANALYZERS          ERROR NORMALIZER          UNIVERSAL ERROR MODEL
(Python AST/Ruff/Bandit,     (Language mappings)       (Standard JSON schema)
 JS AST, Generic)                 │
   │                              ▼
   └────────────────────► ROOT CAUSE ANALYZER
                                  │
                                  ▼
                         PREDICTIVE ENGINE
                                  │
                                  ▼
                          DIAGNOSIS ENGINE
                                  │
                                  ▼
                          FIX GENERATOR (Code Surgery)
                                  │
                                  ▼
                     FIX VERIFICATION ENGINE (Safe static/AST runner)
                                  │
                                  ▼
                        HEALTH SCORE ENGINE (30% Correctness, 20% Security...)
                                  │
                                  ▼
                         ERROR DNA ENGINE (Developer analytics)
                                  │
                                  ▼
                      DATABASE / HISTORY (SQLite/PostgreSQL)
```

## Architectural Principles

1. **Platform Independence**: Core logic resides entirely in `backend/app/core/`. IDE plugins and CLI communicate over REST API or standard interfaces.
2. **Deterministic Offline Fallback**: Static analysis and rule engines provide full diagnosis without external paid AI services.
3. **Safe Execution Verification**: Code fixes are verified through AST re-parsing and rule evaluation without host shell command execution.
