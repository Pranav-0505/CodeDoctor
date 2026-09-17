import difflib
import re

from typing import Tuple

from app.schemas.error_model import DiagnosticItem


class CodeSurgeryEngine:
    """
    Automatic Code Repair & Patch Generation Engine.

    Generates minimal patches, unified diffs, and previews
    without overwriting files blindly.
    """

    @staticmethod
    def generate_fix(
        code: str,
        issue: DiagnosticItem
    ) -> Tuple[str, str, str]:
        """
        Returns:
            (patched_code, diff_patch, summary_of_changes)
        """

        lines = code.splitlines(keepends=True)

        if not lines:
            return code, "", "No code provided to repair."

        target_line_idx = max(0, issue.line - 1)

        if target_line_idx >= len(lines):
            target_line_idx = len(lines) - 1

        original_line = lines[target_line_idx]

        # ---------------------------------------------------------
        # 1. Use issue's corrected_code if available
        # ---------------------------------------------------------
        if issue.corrected_code:
            replacement_line = issue.corrected_code.strip() + "\n"

        # ---------------------------------------------------------
        # 2. Python syntax error repair
        # ---------------------------------------------------------
        elif issue.rule_id == "PY-E901":
            replacement_line = re.sub(
                r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(:",
                r"def \1():",
                original_line
            )

        # ---------------------------------------------------------
        # 3. Predictive out-of-bounds list access
        # Example:
        #     numbers[5]
        # becomes:
        #     numbers[0]
        # ---------------------------------------------------------
        elif issue.rule_id == "PRED-001":
            replacement_line = re.sub(
                r"\[([0-9]+)\]",
                "[0]",
                original_line
            )

        # ---------------------------------------------------------
        # 4. Division/modulo by a known-zero variable
        #
        # Example:
        #     y = 0
        #     result = x / y
        #
        # becomes:
        #     y = 0
        #     if y != 0:
        #         result = x / y
        # ---------------------------------------------------------
        elif issue.rule_id == "LOGIC-001":
            match = re.search(
                r"^(\s*)(.+?)\s*([/%])\s*([A-Za-z_][A-Za-z0-9_]*)\s*$",
                original_line.rstrip("\r\n")
            )

            if match:
                indentation = match.group(1)
                expression = match.group(2).strip()
                operator = match.group(3)
                divisor_name = match.group(4)

                replacement_line = (
                    f"{indentation}if {divisor_name} != 0:\n"
                    f"{indentation}    {expression} {operator} {divisor_name}\n"
                )
            else:
                replacement_line = original_line

        # ---------------------------------------------------------
        # 5. Hardcoded secret repair
        # ---------------------------------------------------------
        elif "SEC-SECRET" in issue.id:
            var_name = (
                original_line.split("=")[0].strip()
                if "=" in original_line
                else "SECRET"
            )

            replacement_line = (
                f'import os\n'
                f'{var_name} = os.getenv("{var_name.upper()}", "")\n'
            )

        # ---------------------------------------------------------
        # 6. JavaScript optional chaining repair
        # ---------------------------------------------------------
        elif "JS-TYPE-NULLPROP" in issue.id:
            replacement_line = original_line.replace(".", "?.")

        # ---------------------------------------------------------
        # 7. JavaScript XSS repair
        # ---------------------------------------------------------
        elif "JS-SEC-XSS" in issue.id:
            replacement_line = original_line.replace(
                ".innerHTML",
                ".textContent"
            )

        # ---------------------------------------------------------
        # 8. Generic fallback
        # ---------------------------------------------------------
        else:
            replacement_line = (
                f"# Code Doctor: {issue.title}\n"
                + original_line
            )

        # ---------------------------------------------------------
        # Construct patched code
        # ---------------------------------------------------------
        patched_lines = (
            lines[:target_line_idx]
            + [replacement_line]
            + lines[target_line_idx + 1:]
        )

        patched_code = "".join(patched_lines)

        # ---------------------------------------------------------
        # Generate unified diff
        # ---------------------------------------------------------
        diff = difflib.unified_diff(
            lines,
            patched_lines,
            fromfile=f"a/{issue.file}",
            tofile=f"b/{issue.file}",
            lineterm=""
        )

        diff_patch = "\n".join(diff)

        summary = (
            f"Code Surgery modified line {issue.line}: "
            f"Replaced '{original_line.strip()}' with "
            f"'{replacement_line.strip()}'."
        )

        return patched_code, diff_patch, summary