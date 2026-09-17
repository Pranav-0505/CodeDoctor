from typing import List, Tuple
from app.schemas.error_model import DiagnosticItem, ErrorCategory

class RootCauseAnalyzer:
    """
    Analyzes list of diagnostics to identify primary root cause
    and categorize cascading downstream errors.
    """
    
    @staticmethod
    def process_cascading_errors(diagnostics: List[DiagnosticItem]) -> Tuple[List[DiagnosticItem], List[DiagnosticItem]]:
        if not diagnostics:
            return [], []

        # Sort diagnostics by line number and severity
        sorted_items = sorted(diagnostics, key=lambda x: (x.line, 0 if x.category == ErrorCategory.SYNTAX else 1))

        root_causes: List[DiagnosticItem] = []
        cascading_issues: List[DiagnosticItem] = []

        primary_root: DiagnosticItem = sorted_items[0]
        primary_root.is_root_cause = True
        root_causes.append(primary_root)

        for item in sorted_items[1:]:
            # If an item occurs on a later line or is dependent on the primary root cause
            if item.category in (ErrorCategory.TYPE, ErrorCategory.RUNTIME, ErrorCategory.LOGIC) and primary_root.category in (ErrorCategory.SYNTAX, ErrorCategory.DEPENDENCY, ErrorCategory.SECURITY):
                item.is_root_cause = False
                item.parent_issue_id = primary_root.id
                item.root_cause = f"Downstream consequence of root cause ({primary_root.title} on line {primary_root.line})"
                cascading_issues.append(item)
            else:
                item.is_root_cause = True
                root_causes.append(item)

        return root_causes, cascading_issues
