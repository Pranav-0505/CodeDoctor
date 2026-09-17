from abc import ABC, abstractmethod
from typing import List
from app.schemas.error_model import DiagnosticItem

class BaseAnalyzer(ABC):
    """
    Abstract Base Class for language-specific static analyzers.
    Target integrations produce standardized DiagnosticItem list.
    """
    
    @property
    @abstractmethod
    def language(self) -> str:
        """Returns the primary language handled by this analyzer."""
        pass

    @abstractmethod
    def analyze(self, code: str, file_path: str = "snippet.py") -> List[DiagnosticItem]:
        """
        Analyze code and return normalized DiagnosticItem list adhering to Universal Error Model.
        """
        pass
