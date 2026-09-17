from fastapi import APIRouter
from app.core.surgery import CodeSurgeryEngine
from app.schemas.fix import SurgeryFixRequest, SurgeryFixResponse
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory

router = APIRouter(tags=["Code Surgery"])

@router.post("/fix", response_model=SurgeryFixResponse)
def generate_code_fix(req: SurgeryFixRequest):
    mock_item = DiagnosticItem(
        id=req.issue_id,
        rule_id=req.rule_id,
        language=req.language,
        file="snippet.py",
        line=req.line,
        column=1,
        severity=SeverityLevel.HIGH,
        category=ErrorCategory.RUNTIME,
        title="Diagnostic Issue",
        message="Target repair requested",
        suggested_fix=req.suggested_fix
    )
    patched_code, diff_patch, summary = CodeSurgeryEngine.generate_fix(req.code, mock_item)
    return SurgeryFixResponse(
        issue_id=req.issue_id,
        original_code=req.code,
        patched_code=patched_code,
        diff_patch=diff_patch,
        summary_of_changes=summary,
        can_auto_verify=True
    )
