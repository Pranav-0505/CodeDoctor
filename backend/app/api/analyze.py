from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.engine import CodeDoctorEngine
from app.models.scan import FileScan
from app.models.diagnosis import Diagnosis as DiagnosisModel
from app.schemas.diagnosis import CodeAnalyzeRequest, DiagnosticResponse

router = APIRouter(tags=["Analysis"])
engine = CodeDoctorEngine()

@router.post("/analyze", response_model=DiagnosticResponse)
@router.post("/diagnose", response_model=DiagnosticResponse)
def analyze_code(req: CodeAnalyzeRequest, db: Session = Depends(get_db)):
    res = engine.diagnose_code(
        code=req.code,
        language=req.language,
        file_path=req.file_path or "snippet.py",
        learning_level=req.learning_level or "Beginner"
    )

    # Persist scan to database
    file_scan = FileScan(
        scan_uuid=res.scan_id,
        file_path=res.file_path,
        language=res.language,
        code_content=req.code,
        total_issues=res.total_issues,
        critical_issues=res.critical_issues,
        security_issues=res.security_issues,
        performance_issues=res.performance_issues,
        health_score=res.health_score,
        platform=req.platform or "web"
    )
    db.add(file_scan)
    db.commit()
    db.refresh(file_scan)

    # Persist diagnoses to database
    for item in res.issues:
        diag = DiagnosisModel(
            scan_id=file_scan.id,
            rule_id=item.rule_id,
            language=item.language,
            file_path=item.file,
            line=item.line,
            column=item.column,
            severity=item.severity,
            category=item.category,
            title=item.title,
            message=item.message,
            root_cause=item.root_cause,
            explanation=item.explanation,
            impact=item.impact,
            confidence=item.confidence,
            suggested_fix=item.suggested_fix,
            corrected_code=item.corrected_code,
            is_root_cause=item.is_root_cause
        )
        db.add(diag)
    db.commit()

    return res
