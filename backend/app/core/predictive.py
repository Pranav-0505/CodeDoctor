from typing import List
from app.schemas.error_model import DiagnosticItem, ErrorCategory, SeverityLevel

class PredictiveAnalysisEngine:
    """
    Predictive Static Analysis Layer.
    Detects potential bugs and runtime hazards before execution.
    """
    
    @staticmethod
    def enhance_predictions(diagnostics: List[DiagnosticItem]) -> List[DiagnosticItem]:
        enhanced: List[DiagnosticItem] = []
        for item in diagnostics:
            # Statically label predictive findings honestly
            if item.rule_id.startswith("PRED-") or item.category in (ErrorCategory.RUNTIME, ErrorCategory.LOGIC):
                item.message = f"[Predictive Static Analysis] {item.message}"
            enhanced.append(item)
        return enhanced
