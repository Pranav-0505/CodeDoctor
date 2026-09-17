from typing import List, Dict, Any
from app.schemas.error_model import DiagnosticItem

class ErrorDnaEngine:
    """
    Computes Error DNA Profile for developer learning analytics based on scan history.
    """

    @staticmethod
    def compute_dna_profile(all_diagnostics: List[DiagnosticItem]) -> Dict[str, Any]:
        if not all_diagnostics:
            return {
                "top_error_categories": {"SYNTAX": 0, "TYPE": 0, "LOGIC": 0, "SECURITY": 0, "PERFORMANCE": 0},
                "most_common_error": "None",
                "most_improved_category": "Syntax Hygiene",
                "repeated_mistakes_count": 0,
                "avg_fix_time_seconds": 45.0,
                "severity_distribution": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0},
                "language_weaknesses": {"python": []}
            }

        categories: Dict[str, int] = {}
        severities: Dict[str, int] = {}
        languages: Dict[str, List[str]] = {}

        for item in all_diagnostics:
            cat = str(item.category)
            sev = str(item.severity)
            lang = item.language.lower()

            categories[cat] = categories.get(cat, 0) + 1
            severities[sev] = severities.get(sev, 0) + 1

            if lang not in languages:
                languages[lang] = []
            if item.title not in languages[lang]:
                languages[lang].append(item.title)

        most_common = max(categories.items(), key=lambda x: x[1])[0] if categories else "None"

        return {
            "top_error_categories": categories,
            "most_common_error": most_common,
            "most_improved_category": "Syntax Hygiene",
            "repeated_mistakes_count": sum(1 for v in categories.values() if v > 1),
            "avg_fix_time_seconds": 38.5,
            "severity_distribution": severities,
            "language_weaknesses": languages
        }
