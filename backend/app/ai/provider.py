from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class AIProvider(ABC):
    """Abstract interface for AI diagnostic assistance."""
    
    @abstractmethod
    def explain_error(self, code: str, title: str, message: str, level: str = "Beginner") -> str:
        pass

    @abstractmethod
    def suggest_fix(self, code: str, title: str, message: str) -> Optional[str]:
        pass
