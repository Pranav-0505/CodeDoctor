from app.core.health_score import HealthScoreEngine
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory

def test_health_score_calculation():
    diagnostics = [
        DiagnosticItem(
            id="1", rule_id="SEC-001", language="python", file="test.py",
            line=1, column=1, severity=SeverityLevel.HIGH, category=ErrorCategory.SECURITY,
            title="Secret", message="Exposed secret"
        )
    ]
    report = HealthScoreEngine.calculate(diagnostics)
    assert report.scores.overall_score < 100.0
    assert report.scores.security_score < 100.0
    assert report.scores.correctness_score == 100.0
