import re
from typing import List
from app.analyzers.base import BaseAnalyzer
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory

class GenericAnalyzer(BaseAnalyzer):
    def __init__(self, target_language: str = "generic"):
        self._language = target_language.lower()

    @property
    def language(self) -> str:
        return self._language

    def analyze(self, code: str, file_path: str = "snippet.txt") -> List[DiagnosticItem]:
        diagnostics: List[DiagnosticItem] = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, 1):
            stripped = line.strip()

            # Hardcoded API keys / Passwords
            if re.search(r'(api_key|password|secret|auth_key)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']', stripped, re.IGNORECASE):
                diagnostics.append(DiagnosticItem(
                    id=f"GEN-SEC-SECRET-{idx}",
                    rule_id="GEN-SEC-001",
                    language=self.language,
                    file=file_path,
                    line=idx,
                    column=1,
                    severity=SeverityLevel.HIGH,
                    category=ErrorCategory.SECURITY,
                    title="Exposed Hardcoded Secret",
                    message="Potential secret or API token hardcoded in source file.",
                    root_cause="Sensitive token stored in plaintext code.",
                    explanation="Hardcoding secrets in source code poses data leak risks.",
                    impact="Potential unauthorized access.",
                    confidence=0.85,
                    suggested_fix="Move secret to external environment configuration.",
                    corrected_code=None,
                    verification_status="UNVERIFIED",
                    is_root_cause=True
                ))

            # TODO / FIX ME indicators
            if re.search(r'\b(FIXME|HACK|BROKEN)\b', stripped):
                diagnostics.append(DiagnosticItem(
                    id=f"GEN-STYLE-FIXME-{idx}",
                    rule_id="GEN-STYLE-001",
                    language=self.language,
                    file=file_path,
                    line=idx,
                    column=1,
                    severity=SeverityLevel.LOW,
                    category=ErrorCategory.STYLE,
                    title="Unresolved FIXME / HACK Marker",
                    message=f"Found code marker: '{stripped}'",
                    root_cause="Work-in-progress code left in file.",
                    explanation="FIXME markers indicate unfinished code logic or known technical debt.",
                    impact="Potential unexpected behavior in production.",
                    confidence=1.0,
                    suggested_fix="Address the underlying technical debt and remove FIXME marker.",
                    corrected_code=None,
                    verification_status="UNVERIFIED",
                    is_root_cause=True
                ))

        return diagnostics
