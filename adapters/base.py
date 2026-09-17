from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PlatformAdapter(ABC):
    """
    Unified Platform Adapter Interface for Code Doctor Engine.
    Allows IDE plugins, CLI, and CI/CD tools to communicate seamlessly.
    """

    @abstractmethod
    def get_code(()) -> str:
        """Extract active source code from platform buffer."""
        pass

    @abstractmethod
    def get_file_path(()) -> str:
        """Get current active file path."""
        pass

    @abstractmethod
    def publish_diagnostics(self, diagnostics: Dict[str, Any]) -> None:
        """Publish diagnostic markers to platform UI."""
        pass

    @abstractmethod
    def apply_patch(self, patch_diff: str) -> bool:
        """Apply verified Code Surgery patch to target platform buffer."""
        pass

    @abstractmethod
    def show_message(self, message: str, level: str = "info") -> None:
        """Display notification message in platform interface."""
        pass
