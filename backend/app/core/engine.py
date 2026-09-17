import uuid
from typing import List, Dict, Any
from app.analyzers import get_analyzer_for_language
from app.core.root_cause import RootCauseAnalyzer
from app.core.predictive import PredictiveAnalysisEngine
from app.core.health_score import HealthScoreEngine
from app.core.learning_mode import LearningExplanationAdapter
from app.ai import get_ai_provider
from app.schemas.diagnosis import DiagnosticResponse
from app.schemas.error_model import DiagnosticItem

class CodeDoctorEngine:
    """
    Central Reusable Code Doctor Engine.
    Orchestrates analyzers, root cause resolution, predictive analysis,
    health scores, AI explanations, and learning modes.
    """

    def __init__(self):
        self.ai_provider = get_ai_provider()

    def diagnose_code(
        self,
        code: str,
        language: str = "python",
        file_path: str = "snippet.py",
        learning_level: str = "Beginner"
    ) -> DiagnosticResponse:
        scan_id = str(uuid.uuid4())
        
        # 1. Run pluggable analyzer for language
        analyzer = get_analyzer_for_language(language)
        raw_diagnostics = analyzer.analyze(code, file_path)

        # 2. Run predictive static analysis enhancement
        diagnostics = PredictiveAnalysisEngine.enhance_predictions(raw_diagnostics)

        # 3. Adapt explanations for selected learning level
        for item in diagnostics:
            item.explanation = LearningExplanationAdapter.adapt_explanation(item, learning_level)
            if self.ai_provider and not item.explanation:
                item.explanation = self.ai_provider.explain_error(code, item.title, item.message, learning_level)

        # 4. Perform Root Cause Analysis on cascading errors
        root_causes, cascading = RootCauseAnalyzer.process_cascading_errors(diagnostics)

        # 5. Compute transparent Code Health Score
        health_report = HealthScoreEngine.calculate(diagnostics, scanned_files_count=1)

        # Issue counters
        crit_count = sum(1 for d in diagnostics if d.severity == "CRITICAL")
        sec_count = sum(1 for d in diagnostics if d.category == "SECURITY")
        perf_count = sum(1 for d in diagnostics if d.category == "PERFORMANCE")

        return DiagnosticResponse(
            scan_id=scan_id,
            file_path=file_path,
            language=language,
            total_issues=len(diagnostics),
            critical_issues=crit_count,
            security_issues=sec_count,
            performance_issues=perf_count,
            health_score=health_report.scores.overall_score,
            issues=diagnostics,
            root_causes=root_causes,
            cascading_issues=cascading,
            learning_level=learning_level
        )
