# Code Doctor Security Model

## Security Principles

1. **Host Safety**: Never execute arbitrary user-provided untrusted code directly on host machines. Verification uses safe AST parsing and rule re-evaluation.
2. **Secret Scrubbing**: Sensitive keys, passwords, and tokens are automatically redacted via `SensitiveDataRedactor` prior to external AI API calls.
3. **Path Traversal Protection**: Project Scanner validates paths with `is_safe_path()` to ensure operations remain bounded within project roots.
4. **Gitignore Compliance**: Excludes `.git`, `node_modules`, `venv`, `cache`, and secret files automatically.
