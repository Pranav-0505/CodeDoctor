from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.error_dna import ErrorDnaEngine
from app.models.diagnosis import Diagnosis as DiagnosisModel

router = APIRouter(tags=["Error DNA"])

@router.get("/error-dna")
def get_error_dna(db: Session = Depends(get_db)):
    diagnoses = db.query(DiagnosisModel).order_by(DiagnosisModel.created_at.desc()).limit(100).all()

    items = []
    for d in diagnoses:
        items.append(d)

    profile = ErrorDnaEngine.compute_dna_profile(items)
    return profile
