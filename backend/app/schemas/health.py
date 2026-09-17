from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class HealthScoreBreakdown(BaseModel):
    overall_score: float = Field(..., description="Overall Code Health Score (0-100)")
    correctness_score: float = Field(..., description="Correctness sub-score (Weight: 30%)")
    security_score: float = Field(..., description="Security sub-score (Weight: 20%)")
    maintainability_score: float = Field(..., description="Maintainability sub-score (Weight: 20%)")
    performance_score: float = Field(..., description="Performance sub-score (Weight: 15%)")
    quality_score: float = Field(..., description="Code Quality sub-score (Weight: 15%)")
    formula_weights: Dict[str, float] = Field(
        default={
            "correctness": 0.30,
            "security": 0.20,
            "maintainability": 0.20,
            "performance": 0.15,
            "quality": 0.15
        },
        description="Transparent score weighting"
    )

class HealthReportResponse(BaseModel):
    project_id: Optional[int] = None
    project_name: Optional[str] = "Current Scan"
    scanned_files_count: int = 1
    scores: HealthScoreBreakdown
    critical_issues_count: int = 0
    total_issues_count: int = 0
    recommendations: List[str] = []
