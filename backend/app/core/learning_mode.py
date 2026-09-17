from app.schemas.error_model import DiagnosticItem

class LearningExplanationAdapter:
    """
    Adapts explanations according to user learning level: Beginner, Intermediate, Advanced.
    """

    @staticmethod
    def adapt_explanation(item: DiagnosticItem, level: str = "Beginner") -> str:
        level = (level or "Beginner").capitalize()

        if level == "Beginner":
            if "IndexError" in item.title or "PRED-001" in item.rule_id:
                return "An index is the position of an item in a list starting from 0. Accessing an index larger than your list length causes Python to crash."
            elif "Syntax" in item.title:
                return "Syntax rules are like grammar rules in English. Check for missing colons ':', parenthesis '()', or unmatched quotes."
            elif "Secret" in item.title:
                return "Never write passwords or API keys directly in code files! If you post your code online, anyone can steal your key."
            return f"Beginner Friendly Note: {item.message}"

        elif level == "Intermediate":
            if "IndexError" in item.title or "PRED-001" in item.rule_id:
                return f"List index out of bounds error. Always verify container length `len(arr)` before indexing elements."
            elif "Secret" in item.title:
                return "Hardcoded secret key detected. Refactor to read from environment variables or a secrets manager."
            return f"Intermediate Diagnostic: {item.message}"

        else:  # Advanced
            if "IndexError" in item.title or "PRED-001" in item.rule_id:
                return "Static bounds analysis indicates a potentially invalid index access exceeding statically known container boundaries."
            elif "Secret" in item.title:
                return "Static analysis rule SEC-001 flagged plaintext secret assignment. Risk: Repository credential leakage."
            return f"Advanced Diagnostic: Rule [{item.rule_id}] triggered. {item.message}"
