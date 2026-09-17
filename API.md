# Code Doctor REST API Reference

Base Endpoint: `http://127.0.0.1:8000/api/v1`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user account |
| POST | `/api/v1/auth/login` | Authenticate user and return JWT |
| GET | `/api/v1/auth/me` | Fetch authenticated user profile |
| POST | `/api/v1/analyze` | Submit source code for diagnostic analysis |
| POST | `/api/v1/diagnose` | Alias for code analysis endpoint |
| POST | `/api/v1/fix` | Generate Code Surgery patch and diff preview |
| POST | `/api/v1/verify` | Safely verify patch syntax and rule clean status |
| POST | `/api/v1/project/scan` | Scan uploaded project or local folder |
| GET | `/api/v1/history` | Retrieve historical scan log records |
| GET | `/api/v1/health-score` | Retrieve Code Health Score breakdown |
| GET | `/api/v1/error-dna` | Retrieve developer Error DNA profile |
| GET | `/api/v1/languages` | List supported analyzer languages |
| GET | `/api/v1/platforms` | List supported client platform adapters |
