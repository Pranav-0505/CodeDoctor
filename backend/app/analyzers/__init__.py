from typing import Dict, Type
from app.analyzers.base import BaseAnalyzer
from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.javascript_analyzer import JavaScriptAnalyzer
from app.analyzers.generic_analyzer import GenericAnalyzer

ANALYZERS: Dict[str, Type[BaseAnalyzer]] = {
    "python": PythonAnalyzer,
    "py": PythonAnalyzer,
    "javascript": JavaScriptAnalyzer,
    "js": JavaScriptAnalyzer,
    "typescript": JavaScriptAnalyzer,
    "ts": JavaScriptAnalyzer,
}

def get_analyzer_for_language(language: str) -> BaseAnalyzer:
    lang_key = (language or "python").lower()
    analyzer_cls = ANALYZERS.get(lang_key)
    if analyzer_cls:
        return analyzer_cls()
    return GenericAnalyzer(target_language=lang_key)

__all__ = [
    "BaseAnalyzer",
    "PythonAnalyzer",
    "JavaScriptAnalyzer",
    "GenericAnalyzer",
    "get_analyzer_for_language"
]
