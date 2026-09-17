from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.error_model import DiagnosticItem

class CodeAnalyzeRequest(BaseModel):
    code: str = Field(..., description="Source code snippet to analyze")
    language: str = Field("python", description="Programming language (python, javascript, etc.)")
    file_path: Optional[str] = Field("snippet.py", description="Virtual or actual file path")
    learning_level: Optional[str] = Field("Beginner", description="Beginner, Intermediate, Advanced")
    platform: Optional[str] = Field("web", description="Client platform identifier (web, cli, vscode, etc.)")

class ProjectScanRequest(BaseModel):
    project_path: Optional[str] = Field(None, description="Local folder path for project scan")
    files: Optional[Dict[str, str]] = Field(None, description="Dict of filename -> content for uploaded projects")
    project_name: Optional[str] = Field("My Project", description="Name of the project")
    learning_level: Optional[str] = Field("Beginner", description="Beginner, Intermediate, Advanced")

class DiagnosticResponse(BaseModel):
    scan_id: str
    file_path: str
    language: str
    total_issues: int
    critical_issues: int
    security_issues: int
    performance_issues: int
    health_score: float
    issues: List[DiagnosticItem]
    root_causes: List[DiagnosticItem]
    cascading_issues: List[DiagnosticItem]
    learning_level: str
