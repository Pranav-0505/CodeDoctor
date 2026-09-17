import os
from typing import Dict, Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.engine import CodeDoctorEngine
from app.core.health_score import HealthScoreEngine
from app.models.scan import FileScan
from app.models.diagnosis import Diagnosis as DiagnosisModel
from app.utils.file_system import load_gitignore, should_scan_file
from app.schemas.diagnosis import ProjectScanRequest
from app.schemas.error_model import DiagnosticItem


router = APIRouter(
    prefix="/project",
    tags=["Project Scanner"]
)

engine = CodeDoctorEngine()


def normalize_language(file_path: str) -> str:
    """
    Convert file extensions into the language names expected
    by the CodeDoctor analyzer.
    """

    ext = os.path.splitext(file_path)[1].lstrip(".").lower()

    language_map = {
        "py": "python",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "java": "java",
        "c": "c",
        "h": "c",
        "cpp": "cpp",
        "cc": "cpp",
        "cxx": "cpp",
        "hpp": "cpp",
        "go": "go",
        "rs": "rust",
        "rb": "ruby",
        "php": "php",
        "swift": "swift",
        "kt": "kotlin",
        "kts": "kotlin",
        "cs": "csharp",
        "html": "html",
        "css": "css",
        "sql": "sql"
    }

    return language_map.get(ext, ext or "python")


def save_scan_results(
    db: Session,
    diag_res: Any,
    content: str
) -> None:
    """
    Save one FileScan and all of its Diagnosis records.
    """

    file_scan = FileScan(
        scan_uuid=diag_res.scan_id,
        file_path=diag_res.file_path,
        language=diag_res.language,
        code_content=content,
        total_issues=diag_res.total_issues,
        critical_issues=diag_res.critical_issues,
        security_issues=diag_res.security_issues,
        performance_issues=diag_res.performance_issues,
        health_score=diag_res.health_score,
        platform="web"
    )

    db.add(file_scan)
    db.commit()
    db.refresh(file_scan)

    for item in diag_res.issues:
        diagnosis = DiagnosisModel(
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

        db.add(diagnosis)

    db.commit()


def calculate_project_health(results: List[Dict[str, Any]]) -> float:
    """
    Calculate project health using the same HealthScoreEngine
    used by individual code diagnoses.
    """

    diagnostics: List[DiagnosticItem] = []

    for result in results:
        for item in result.get("issues", []):
            diagnostics.append(
                DiagnosticItem(
                    id=str(item.get("id", "")),
                    rule_id=item.get("rule_id", ""),
                    language=item.get("language", "python"),
                    file=item.get("file", "unknown"),
                    line=item.get("line", 1),
                    column=item.get("column", 1),
                    severity=item.get("severity", "INFO"),
                    category=item.get("category", "STYLE"),
                    title=item.get("title", ""),
                    message=item.get("message", ""),
                    root_cause=item.get("root_cause", ""),
                    explanation=item.get("explanation", ""),
                    impact=item.get("impact", ""),
                    confidence=item.get("confidence", 1.0),
                    suggested_fix=item.get("suggested_fix", ""),
                    corrected_code=item.get("corrected_code"),
                    is_root_cause=item.get("is_root_cause", True),
                    parent_issue_id=item.get("parent_issue_id")
                )
            )

    report = HealthScoreEngine.calculate(
        diagnostics=diagnostics,
        scanned_files_count=max(len(results), 1)
    )

    return report.scores.overall_score


@router.post("/scan")
def scan_project(
    req: ProjectScanRequest,
    db: Session = Depends(get_db)
):
    results: List[Dict[str, Any]] = []

    total_issues = 0
    critical_issues = 0
    scanned_files = 0

    # ---------------------------------------------------------
    # 1. Direct code files provided in the request
    # ---------------------------------------------------------
    if req.files:
        for file_path, content in req.files.items():

            if not should_scan_file(file_path):
                continue

            scanned_files += 1

            language = normalize_language(file_path)

            diag_res = engine.diagnose_code(
                content,
                language=language,
                file_path=file_path,
                learning_level=req.learning_level or "Beginner"
            )

            total_issues += diag_res.total_issues
            critical_issues += diag_res.critical_issues

            save_scan_results(
                db=db,
                diag_res=diag_res,
                content=content
            )

            results.append(diag_res.dict())

    # ---------------------------------------------------------
    # 2. Local folder/project path scan
    # ---------------------------------------------------------
    elif req.project_path and os.path.exists(req.project_path):

        gitignore_spec = load_gitignore(req.project_path)

        for root, _, files in os.walk(req.project_path):

            for file_name in files:

                full_path = os.path.join(root, file_name)

                rel_path = os.path.relpath(
                    full_path,
                    req.project_path
                )

                if not should_scan_file(
                    rel_path,
                    gitignore_spec
                ):
                    continue

                try:
                    with open(
                        full_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:
                        content = f.read()

                    language = normalize_language(file_name)

                    diag_res = engine.diagnose_code(
                        content,
                        language=language,
                        file_path=rel_path,
                        learning_level=req.learning_level or "Beginner"
                    )

                    scanned_files += 1
                    total_issues += diag_res.total_issues
                    critical_issues += diag_res.critical_issues

                    save_scan_results(
                        db=db,
                        diag_res=diag_res,
                        content=content
                    )

                    results.append(diag_res.dict())

                except Exception:
                    # Ignore files that cannot be read or analyzed.
                    continue

    # ---------------------------------------------------------
    # 3. Fallback demo scan
    # ---------------------------------------------------------
    else:

        demo_code = (
            "my_list = [1, 2, 3]\n"
            "print(my_list[5])"
        )

        diag_res = engine.diagnose_code(
            demo_code,
            language="python",
            file_path="demo.py",
            learning_level="Beginner"
        )

        scanned_files = 1
        total_issues = diag_res.total_issues
        critical_issues = diag_res.critical_issues

        save_scan_results(
            db=db,
            diag_res=diag_res,
            content=demo_code
        )

        results.append(diag_res.dict())

    # ---------------------------------------------------------
    # Overall project health
    # ---------------------------------------------------------
    overall_health = calculate_project_health(results)

    return {
        "project_name": req.project_name or "Scanned Project",
        "scanned_files_count": scanned_files,
        "total_issues": total_issues,
        "critical_issues": critical_issues,
        "health_score": overall_health,
        "file_results": results
    }