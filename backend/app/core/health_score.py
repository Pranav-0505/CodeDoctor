from typing import List
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory
from app.schemas.health import HealthScoreBreakdown, HealthReportResponse

class HealthScoreEngine:
    """
    Computes transparent Code Health Score (0-100) using weighted category deductions:
    - Correctness (30%)
    - Security (20%)
    - Maintainability (20%)
    - Performance (15%)
    - Quality (15%)
    """

    SEVERITY_DEDUCTIONS = {
        SeverityLevel.CRITICAL: 25.0,
        SeverityLevel.HIGH: 15.0,
        SeverityLevel.MEDIUM: 8.0,
        SeverityLevel.LOW: 3.0,
        SeverityLevel.INFO: 0.0
    }

    @classmethod
    def calculate(cls, diagnostics: List[DiagnosticItem], scanned_files_count: int = 1) -> HealthReportResponse:
        correctness_deduction = 0.0
        security_deduction = 0.0
        maintainability_deduction = 0.0
        performance_deduction = 0.0
        quality_deduction = 0.0

        critical_count = 0

        for item in diagnostics:
            deduction = cls.SEVERITY_DEDUCTIONS.get(item.severity, 5.0)
            if item.severity == SeverityLevel.CRITICAL:
                critical_count += 1

            if item.category in (ErrorCategory.SYNTAX, ErrorCategory.RUNTIME, ErrorCategory.LOGIC, ErrorCategory.TYPE):
                correctness_deduction += deduction
            elif item.category == ErrorCategory.SECURITY:
                security_deduction += deduction
            elif item.category == ErrorCategory.PERFORMANCE:
                performance_deduction += deduction
            elif item.category in (ErrorCategory.STYLE, ErrorCategory.CONFIGURATION):
                quality_deduction += deduction
            else:
                maintainability_deduction += deduction

        # Sub-scores clamped between 0 and 100
        correctness_score = max(0.0, round(100.0 - correctness_deduction, 1))
        security_score = max(0.0, round(100.0 - security_deduction, 1))
        maintainability_score = max(0.0, round(100.0 - maintainability_deduction, 1))
        performance_score = max(0.0, round(100.0 - performance_deduction, 1))
        quality_score = max(0.0, round(100.0 - quality_deduction, 1))

        # Overall Weighted Score Formula
        overall_score = round(
            (correctness_score * 0.30) +
            (security_score * 0.20) +
            (maintainability_score * 0.20) +
            (performance_score * 0.15) +
            (quality_score * 0.15),
            1
        )

        recommendations = []
        if security_score < 80.0:
            recommendations.append("Security Warning: Resolve exposed secrets and potential SQL injections.")
        if correctness_score < 80.0:
            recommendations.append("Correctness Warning: Fix critical syntax and runtime exception risks.")
        if performance_score < 80.0:
            recommendations.append("Performance Optimization: Refactor deeply nested loop structures.")
        if overall_score >= 90.0:
            recommendations.append("Excellent Code Quality! Keep up the great engineering standards.")

        breakdown = HealthScoreBreakdown(
            overall_score=overall_score,
            correctness_score=correctness_score,
            security_score=security_score,
            maintainability_score=maintainability_score,
            performance_score=performance_score,
            quality_score=quality_score
        )

        return HealthReportResponse(
            scanned_files_count=scanned_files_count,
            scores=breakdown,
            critical_issues_count=critical_count,
            total_issues_count=len(diagnostics),
            recommendations=recommendations
        )
