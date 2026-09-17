import re
from typing import List
from app.analyzers.base import BaseAnalyzer
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory

class JavaScriptAnalyzer(BaseAnalyzer):
    @property
    def language(self) -> str:
        return "javascript"

    def analyze(self, code: str, file_path: str = "snippet.js") -> List[DiagnosticItem]:
        diagnostics: List[DiagnosticItem] = []
        lines = code.splitlines()

        # Track bracket balance for syntax
        open_braces = code.count('{')
        close_braces = code.count('}')
        open_parens = code.count('(')
        close_parens = code.count(')')

        if open_braces != close_braces:
            diagnostics.append(DiagnosticItem(
                id="JS-SYNTAX-BRACE",
                rule_id="JS-E901",
                language="javascript",
                file=file_path,
                line=len(lines),
                column=1,
                severity=SeverityLevel.CRITICAL,
                category=ErrorCategory.SYNTAX,
                title="Unbalanced Curly Braces '{ }'",
                message=f"Found {open_braces} opening '{{' and {close_braces} closing '}}' braces.",
                root_cause="Syntax Error: Missing closing or opening curly brace in JavaScript file.",
                explanation="JavaScript requires all code blocks created with '{' to be cleanly closed with '}'.",
                impact="Script fails to parse and execution terminates immediately.",
                confidence=1.0,
                suggested_fix="Ensure all opening braces '{' have matching closing braces '}'.",
                corrected_code=None,
                verification_status="UNVERIFIED",
                is_root_cause=True
            ))

        if open_parens != close_parens:
            diagnostics.append(DiagnosticItem(
                id="JS-SYNTAX-PAREN",
                rule_id="JS-E902",
                language="javascript",
                file=file_path,
                line=len(lines),
                column=1,
                severity=SeverityLevel.CRITICAL,
                category=ErrorCategory.SYNTAX,
                title="Unbalanced Parentheses '( )'",
                message=f"Found {open_parens} opening '(' and {close_parens} closing ')' parentheses.",
                root_cause="Syntax Error: Unmatched parenthesis in function signature or expression.",
                explanation="Parentheses surrounding function calls or conditionals must be balanced.",
                impact="Parse failure SyntaxError in browser or Node.js runtime.",
                confidence=1.0,
                suggested_fix="Balance opening '(' and closing ')' parentheses.",
                corrected_code=None,
                verification_status="UNVERIFIED",
                is_root_cause=True
            ))

        # Line by line rule checks
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()

            # TypeError: Cannot read properties of undefined/null
            if re.search(r'\b(null|undefined)\.[a-zA-Z0-9_]+', stripped):
                diagnostics.append(DiagnosticItem(
                    id=f"JS-TYPE-NULLPROP-{idx}",
                    rule_id="JS-T001",
                    language="javascript",
                    file=file_path,
                    line=idx,
                    column=1,
                    severity=SeverityLevel.HIGH,
                    category=ErrorCategory.TYPE,
                    title="TypeError: Accessing Property of null / undefined",
                    message="Attempting to access property or method on null or undefined value.",
                    root_cause="Expression explicitly references property on null/undefined.",
                    explanation="In JavaScript, accessing properties of null or undefined raises a runtime TypeError: Cannot read properties of undefined.",
                    impact="Runtime crash when code execution hits this line.",
                    confidence=0.95,
                    suggested_fix="Use optional chaining '?.' or null check before property access.",
                    corrected_code=re.sub(r'(\b[a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)', r'\1?.\2', line),
                    verification_status="UNVERIFIED",
                    is_root_cause=True
                ))

            # Security: innerHTML XSS Risk
            if ".innerHTML" in stripped and "=" in stripped:
                diagnostics.append(DiagnosticItem(
                    id=f"JS-SEC-XSS-{idx}",
                    rule_id="JS-SEC-001",
                    language="javascript",
                    file=file_path,
                    line=idx,
                    column=1,
                    severity=SeverityLevel.HIGH,
                    category=ErrorCategory.SECURITY,
                    title="Cross-Site Scripting (XSS) via innerHTML",
                    message="Direct assignment to element.innerHTML with unescaped content.",
                    root_cause="Raw HTML string dynamically injected into DOM.",
                    explanation="Assigning unescaped user input to innerHTML enables Cross-Site Scripting (XSS), allowing attacker scripts to run in user browsers.",
                    impact="Session hijacking, cookie theft, DOM manipulation.",
                    confidence=0.90,
                    suggested_fix="Use textContent or innerText instead of innerHTML.",
                    corrected_code=line.replace(".innerHTML", ".textContent"),
                    verification_status="UNVERIFIED",
                    is_root_cause=True
                ))

            # Security: Use of eval()
            if re.search(r'\beval\s*\(', stripped):
                diagnostics.append(DiagnosticItem(
                    id=f"JS-SEC-EVAL-{idx}",
                    rule_id="JS-SEC-002",
                    language="javascript",
                    file=file_path,
                    line=idx,
                    column=1,
                    severity=SeverityLevel.CRITICAL,
                    category=ErrorCategory.SECURITY,
                    title="Unsafe JavaScript eval() Execution",
                    message="Use of dangerous global function eval().",
                    root_cause="Code dynamically evaluates strings as JS code.",
                    explanation="eval() executes arbitrary strings with full caller privileges and hinders JS engine performance optimizations.",
                    impact="Arbitrary code execution and severe vulnerability.",
                    confidence=1.0,
                    suggested_fix="Refactor code to avoid eval() using JSON.parse() or function lookup tables.",
                    corrected_code=line.replace("eval(", "JSON.parse("),
                    verification_status="UNVERIFIED",
                    is_root_cause=True
                ))

        return diagnostics
