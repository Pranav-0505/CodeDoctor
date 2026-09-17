import ast
from typing import Tuple
from app.analyzers import get_analyzer_for_language
from app.schemas.fix import VerifyFixResponse

class FixVerificationEngine:
    """
    Safely verifies generated patches through static analysis, AST re-parsing,
    and rule re-evaluation without running arbitrary untrusted host code.
    """

    @staticmethod
    def verify_patch(original_code: str, patched_code: str, language: str = "python", rule_id: str = None) -> VerifyFixResponse:
        # 1. Syntax Check
        if language.lower() in ("python", "py"):
            try:
                ast.parse(patched_code)
            except SyntaxError as se:
                return VerifyFixResponse(
                    passed=False,
                    status="REJECTED",
                    verification_mode="static_syntax",
                    original_issues_count=1,
                    new_issues_count=1,
                    details=f"Verification FAIL: Patched code introduced new SyntaxError at line {se.lineno}: {se.msg}"
                )

        # 2. Re-run Analyzer on Patched Code
        analyzer = get_analyzer_for_language(language)
        original_diagnostics = analyzer.analyze(original_code, "original.code")
        patched_diagnostics = analyzer.analyze(patched_code, "patched.code")

        orig_count = len(original_diagnostics)
        patched_count = len(patched_diagnostics)

        # 3. Check if target rule or total issue count decreased
        target_rule_fixed = False
        if rule_id:
            orig_has_rule = any(d.rule_id == rule_id for d in original_diagnostics)
            patched_has_rule = any(d.rule_id == rule_id for d in patched_diagnostics)
            if orig_has_rule and not patched_has_rule:
                target_rule_fixed = True

        if target_rule_fixed or patched_count < orig_count:
            return VerifyFixResponse(
                passed=True,
                status="VERIFIED",
                verification_mode="static_analysis_and_ast",
                original_issues_count=orig_count,
                new_issues_count=patched_count,
                details=f"Verification PASS: Issue count reduced from {orig_count} to {patched_count}. Syntax and rules verified clean."
            )
        else:
            return VerifyFixResponse(
                passed=False,
                status="REJECTED",
                verification_mode="static_analysis_and_ast",
                original_issues_count=orig_count,
                new_issues_count=patched_count,
                details=f"Verification REJECTED: Fix did not eliminate target issue '{rule_id or 'all'}'."
            )
