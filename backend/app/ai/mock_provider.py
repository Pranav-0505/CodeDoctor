from typing import Optional
from app.ai.provider import AIProvider
from app.ai.redactor import SensitiveDataRedactor

class MockProvider(AIProvider):
    """Offline-first deterministic AI provider fallback."""
    
    def explain_error(self, code: str, title: str, message: str, level: str = "Beginner") -> str:
        clean_code = SensitiveDataRedactor.redact(code)
        if level == "Beginner":
            return f"Code Doctor Diagnostic ({title}): {message}. Check line references and ensure variables are defined before accessing them."
        elif level == "Intermediate":
            return f"Intermediate Analysis: Issue '{title}' occurred due to invalid runtime state. {message}."
        else:
            return f"Advanced Analysis: Static/Dynamic analyzer flagged rule '{title}'. Root cause trace: {message}."

    def suggest_fix(self, code: str, title: str, message: str) -> Optional[str]:
        return "# Code Doctor Fix Recommendation: Validate inputs and bounds before property access."
