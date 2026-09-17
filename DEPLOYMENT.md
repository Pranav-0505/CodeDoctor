# Code Doctor Deployment Guide

## Production Environment Setup

1. **Backend**:
   - Run FastAPI with Uvicorn or Gunicorn behind Nginx reverse proxy.
   - Configure PostgreSQL database via `DATABASE_URL` environment variable.
   - Set production `SECRET_KEY` and optional `GEMINI_API_KEY`.

2. **Frontend**:
   - Build static assets: `cd frontend && npm run build`.
   - Serve static dist folder via Nginx or Cloudflare Pages.

3. **CLI**:
   - Publish CLI to internal PyPI registry or install via `pip install git+https://github.com/org/code-doctor.git#subdirectory=cli`.
