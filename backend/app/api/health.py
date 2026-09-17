from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.health_score import HealthScoreEngine
from app.models.scan import FileScan
from app.models.diagnosis import Diagnosis
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory
from app.schemas.health import HealthReportResponse, HealthScoreBreakdown

router = APIRouter(tags=["Health Score"])


@router.get("/health-score", response_model=HealthReportResponse)
def get_health_score(db: Session = Depends(get_db)):
    recent_scans = (
        db.query(FileScan)
        .order_by(FileScan.created_at.desc())
        .limit(10)
        .all()
    )

    if not recent_scans:
        breakdown = HealthScoreBreakdown(
            overall_score=85.0,
            correctness_score=90.0,
            security_score=80.0,
            maintainability_score=85.0,
            performance_score=85.0,
            quality_score=85.0
        )

        return HealthReportResponse(
            project_name="Demo Workspace",
            scanned_files_count=1,
            scores=breakdown,
            critical_issues_count=0,
            total_issues_count=0,
            recommendations=[
                "All scans clean. Keep up excellent engineering practices!"
            ]
        )

    scan_ids = [scan.id for scan in recent_scans]

    diagnoses = (
        db.query(Diagnosis)
        .filter(Diagnosis.scan_id.in_(scan_ids))
        .all()
    )

    diagnostic_items = []

    for item in diagnoses:
        diagnostic_items.append(
            DiagnosticItem(
                id=str(item.id),
                rule_id=item.rule_id,
                language=item.language,
                file=item.file_path,
                line=item.line or 1,
                column=item.column or 1,
                severity=SeverityLevel(item.severity),
                category=ErrorCategory(item.category),
                title=item.title,
                message=item.message,
                root_cause=item.root_cause,
                explanation=item.explanation,
                impact=item.impact,
                confidence=item.confidence or 1.0,
                suggested_fix=item.suggested_fix,
                corrected_code=item.corrected_code,
                is_root_cause=item.is_root_cause if item.is_root_cause is not None else True,
                parent_issue_id=(
                    str(item.parent_issue_id)
                    if item.parent_issue_id is not None
                    else None
                )
            )
        )

    report = HealthScoreEngine.calculate(
        diagnostics=diagnostic_items,
        scanned_files_count=len(recent_scans)
    )

    return HealthReportResponse(
        project_id=None,
        project_name="Workspace Scans",
        scanned_files_count=report.scanned_files_count,
        scores=report.scores,
        critical_issues_count=report.critical_issues_count,
        total_issues_count=report.total_issues_count,
        recommendations=report.recommendations
    )