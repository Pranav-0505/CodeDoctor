from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SeverityLevel(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ErrorCategory(str, Enum):
    SYNTAX = "SYNTAX"
    TYPE = "TYPE"
    LOGIC = "LOGIC"
    RUNTIME = "RUNTIME"
    MEMORY = "MEMORY"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    STYLE = "STYLE"
    DEPENDENCY = "DEPENDENCY"
    CONFIGURATION = "CONFIGURATION"
    UNKNOWN = "UNKNOWN"

class DiagnosticItem(BaseModel):
    id: str = Field(..., description="Unique issue identifier")
    rule_id: str = Field(..., description="Analyzer rule ID, e.g., PY-E901 or SEC-001")
    language: str = Field(..., description="Source code language")
    file: str = Field(..., description="Target file path")
    line: int = Field(1, ge=1, description="Line number (1-based)")
    column: int = Field(1, ge=1, description="Column number (1-based)")
    severity: SeverityLevel = Field(SeverityLevel.MEDIUM, description="Issue severity")
    category: ErrorCategory = Field(ErrorCategory.UNKNOWN, description="Normalized error category")
    title: str = Field(..., description="Short error title")
    message: str = Field(..., description="Detailed diagnostic message")
    root_cause: Optional[str] = Field(None, description="Explanation of root cause")
    explanation: Optional[str] = Field(None, description="User-friendly explanation tailored to learning level")
    impact: Optional[str] = Field(None, description="Potential impact of the issue")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Analyzer confidence level (0.0 to 1.0)")
    suggested_fix: Optional[str] = Field(None, description="Human-readable fix recommendation")
    corrected_code: Optional[str] = Field(None, description="Minimal corrected code replacement")
    verification_status: str = Field("UNVERIFIED", description="UNVERIFIED, PENDING, VERIFIED, REJECTED")
    is_root_cause: bool = Field(True, description="True if primary root cause, False if downstream consequence")
    parent_issue_id: Optional[str] = Field(None, description="Parent issue ID if cascading error")

    class Config:
        use_enum_values = True
