import os
import pathspec

IGNORED_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "venv", ".venv",
    "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist",
    "out", ".idea", ".vscode", "coverage", ".next"
}

IGNORED_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".exe", ".dll", ".so", ".dylib",
    ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".ico", ".pdf", ".mp4", ".mp3", ".db", ".sqlite"
}

def is_safe_path(base_dir: str, target_path: str) -> bool:
    """Ensure target path is inside base_dir to prevent path traversal."""
    try:
        abs_base = os.path.abspath(base_dir)
        abs_target = os.path.abspath(target_path)
        return abs_target.startswith(abs_base)
    except Exception:
        return False

def load_gitignore(project_path: str):
    """Parse .gitignore file if present."""
    gitignore_file = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_file):
        try:
            with open(gitignore_file, "r", encoding="utf-8", errors="ignore") as f:
                return pathspec.PathSpec.from_lines("gitwildmatch", f)
        except Exception:
            pass
    return None

def should_scan_file(file_path: str, gitignore_spec=None) -> bool:
    """Determine if a file should be scanned based on rules and gitignore."""
    norm_path = file_path.replace("\\", "/")
    parts = norm_path.split("/")
    
    # Check directory ignore list
    for part in parts:
        if part in IGNORED_DIRS:
            return False
            
    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext in IGNORED_EXTENSIONS:
        return False
        
    # Check gitignore spec if available
    if gitignore_spec and gitignore_spec.match_file(norm_path):
        return False
        
    return True
