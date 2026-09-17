from typing import Optional
from pydantic import BaseModel, Field

class SurgeryFixRequest(BaseModel):
    code: str = Field(..., description="Original source code")
    issue_id: str = Field(..., description="Target issue identifier")
    rule_id: str = Field(..., description="Rule ID causing the issue")
    language: str = Field("python", description="Programming language")
    line: int = Field(1, ge=1, description="Line number")
    suggested_fix: Optional[str] = Field(None, description="Optional suggested fix snippet")

class SurgeryFixResponse(BaseModel):
    issue_id: str
    original_code: str
    patched_code: str
    diff_patch: str
    summary_of_changes: str
    can_auto_verify: bool

class VerifyFixRequest(BaseModel):
    original_code: str = Field(..., description="Original code before fix")
    patched_code: str = Field(..., description="Fixed code to verify")
    language: str = Field("python", description="Language of the code")
    rule_id: Optional[str] = Field(None, description="Original rule ID")

class VerifyFixResponse(BaseModel):
    passed: bool
    status: str  # VERIFIED, REJECTED, UNKNOWN
    verification_mode: str  # static_syntax, lint, unit_test
    original_issues_count: int
    new_issues_count: int
    details: str
