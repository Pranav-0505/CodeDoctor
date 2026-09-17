import json
import urllib.request
from typing import Optional
from app.ai.provider import AIProvider
from app.ai.redactor import SensitiveDataRedactor
from app.config import settings

class GeminiProvider(AIProvider):
    """Google Gemini AI integration using direct REST client."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    def explain_error(self, code: str, title: str, message: str, level: str = "Beginner") -> str:
        if not self.api_key:
            from app.ai.mock_provider import MockProvider
            return MockProvider().explain_error(code, title, message, level)

        redacted_code = SensitiveDataRedactor.redact(code)
        prompt = (
            f"You are Code Doctor, an expert code diagnosis system.\n"
            f"Explain this issue for a developer at {level} level.\n"
            f"Error Title: {title}\n"
            f"Error Message: {message}\n"
            f"Code Snippet:\n{redacted_code}\n\n"
            f"Keep explanation concise, friendly, and practical."
        )

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            from app.ai.mock_provider import MockProvider
            return MockProvider().explain_error(code, title, message, level)

    def suggest_fix(self, code: str, title: str, message: str) -> Optional[str]:
        if not self.api_key:
            from app.ai.mock_provider import MockProvider
            return MockProvider().suggest_fix(code, title, message)

        redacted_code = SensitiveDataRedactor.redact(code)
        prompt = f"Fix this issue:\n{title} - {message}\nCode:\n{redacted_code}\nReturn ONLY corrected code snippet."

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            from app.ai.mock_provider import MockProvider
            return MockProvider().suggest_fix(code, title, message)
