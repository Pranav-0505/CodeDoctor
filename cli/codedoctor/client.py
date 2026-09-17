import os
import sys

# Add backend directory to sys.path if running locally
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.core.engine import CodeDoctorEngine
from app.core.health_score import HealthScoreEngine
from app.core.surgery import CodeSurgeryEngine
from app.core.verification import FixVerificationEngine
from app.utils.file_system import load_gitignore, should_scan_file

class LocalEngineClient:
    def __init__(self):
        self.engine = CodeDoctorEngine()

    def scan_file(self, file_path: str, learning_level: str = "Beginner"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        ext = os.path.splitext(file_path)[1].lstrip('.').lower() or "python"
        res = self.engine.diagnose_code(code, language=ext, file_path=file_path, learning_level=learning_level)
        return res

    def scan_project(self, project_dir: str, learning_level: str = "Beginner"):
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project directory not found: {project_dir}")
            
        gitignore_spec = load_gitignore(project_dir)
        scanned_files = 0
        all_issues = []

        for root, _, files in os.walk(project_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, project_dir)
                if should_scan_file(rel_path, gitignore_spec):
                    scanned_files += 1
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        ext = os.path.splitext(file_name)[1].lstrip('.').lower() or "python"
                        diag_res = self.engine.diagnose_code(content, language=ext, file_path=rel_path, learning_level=learning_level)
                        all_issues.extend(diag_res.issues)
                    except Exception:
                        pass

        health_report = HealthScoreEngine.calculate(all_issues, scanned_files_count=scanned_files)
        return {
            "project_path": project_dir,
            "scanned_files_count": scanned_files,
            "total_issues": len(all_issues),
            "critical_issues": sum(1 for i in all_issues if i.severity == "CRITICAL"),
            "health_score": health_report.scores.overall_score,
            "issues": [i.dict() for i in all_issues],
            "health_report": health_report.dict()
        }
