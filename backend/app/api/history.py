from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.scan import FileScan

router = APIRouter(tags=["History"])

@router.get("/history")
def get_scan_history(db: Session = Depends(get_db)):
    scans = db.query(FileScan).order_by(FileScan.created_at.desc()).limit(50).all()
    results: List[Dict[str, Any]] = []
    for s in scans:
        results.append({
            "scan_id": s.scan_uuid,
            "file_path": s.file_path,
            "language": s.language,
            "total_issues": s.total_issues,
            "critical_issues": s.critical_issues,
            "security_issues": s.security_issues,
            "performance_issues": s.performance_issues,
            "health_score": s.health_score,
            "platform": s.platform,
            "created_at": s.created_at.isoformat() if s.created_at else None
        })
    return results
