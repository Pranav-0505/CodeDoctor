# Code Doctor Testing Strategy

## Running Backend Test Suite

```bash
cd backend
python -m pytest tests/
```

### Test Coverage

* `test_analyzers.py`: Validates Python syntax, predictive index error, security secrets, performance nested loops, and JavaScript AST rules.
* `test_root_cause.py`: Validates cascading error root cause identification.
* `test_surgery.py`: Validates Code Surgery patch generation and unified diff previews.
* `test_verification.py`: Validates safe fix verification pipeline.
* `test_health_score.py`: Validates weighted Code Health Score calculations.
* `test_api.py`: Integration test suite for FastAPI REST API endpoints.
