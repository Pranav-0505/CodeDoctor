from typing import List, Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Platforms & Languages"])

@router.get("/languages")
def get_supported_languages() -> List[Dict[str, Any]]:
    return [
        {"id": "python", "name": "Python", "analyzer": "PythonAST + Ruff + Bandit", "support": "FULL"},
        {"id": "javascript", "name": "JavaScript", "analyzer": "JavaScript AST & Rules", "support": "FULL"},
        {"id": "typescript", "name": "TypeScript", "analyzer": "TypeScript Rules Engine", "support": "FULL"},
        {"id": "cpp", "name": "C / C++", "analyzer": "Generic Pattern Analyzer", "support": "PARTIAL"},
        {"id": "java", "name": "Java", "analyzer": "Generic Pattern Analyzer", "support": "PARTIAL"},
        {"id": "rust", "name": "Rust", "analyzer": "Generic Pattern Analyzer", "support": "PARTIAL"}
    ]

@router.get("/platforms")
def get_supported_platforms() -> List[Dict[str, Any]]:
    return [
        {"id": "web", "name": "Web Dashboard", "status": "ACTIVE"},
        {"id": "rest_api", "name": "REST API (FastAPI)", "status": "ACTIVE"},
        {"id": "cli", "name": "Python CLI (codedoctor)", "status": "ACTIVE"},
        {"id": "vscode", "name": "VS Code Extension Adapter", "status": "ACTIVE"},
        {"id": "github_actions", "name": "GitHub Actions CI/CD", "status": "ACTIVE"},
        {"id": "jetbrains", "name": "JetBrains IDE Adapter", "status": "PLANNED"},
        {"id": "visualstudio", "name": "Visual Studio Adapter", "status": "PLANNED"},
        {"id": "jupyter", "name": "Jupyter Notebook Adapter", "status": "PLANNED"},
        {"id": "gitlab_ci", "name": "GitLab CI Adapter", "status": "PLANNED"}
    ]
