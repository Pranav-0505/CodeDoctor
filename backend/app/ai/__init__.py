from app.ai.provider import AIProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.mock_provider import MockProvider
from app.ai.redactor import SensitiveDataRedactor
from app.config import settings

def get_ai_provider() -> AIProvider:
    if settings.GEMINI_API_KEY and settings.ENABLE_AI_ENHANCEMENT:
        return GeminiProvider()
    return MockProvider()

__all__ = [
    "AIProvider",
    "GeminiProvider",
    "MockProvider",
    "SensitiveDataRedactor",
    "get_ai_provider"
]
