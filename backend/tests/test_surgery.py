from app.core.surgery import CodeSurgeryEngine
from app.schemas.error_model import DiagnosticItem, SeverityLevel, ErrorCategory

def test_code_surgery_patch_generation():
    original_code = "my_list = [1, 2, 3]\nprint(my_list[5])\n"
    item = DiagnosticItem(
        id="PRED-INDEX-2",
        rule_id="PRED-001",
        language="python",
        file="snippet.py",
        line=2,
        column=1,
        severity=SeverityLevel.HIGH,
        category=ErrorCategory.RUNTIME,
        title="Predictive IndexError",
        message="Index 5 out of bounds"
    )

    patched_code, diff_patch, summary = CodeSurgeryEngine.generate_fix(original_code, item)
    assert patched_code != original_code
    assert "a/snippet.py" in diff_patch
    assert "b/snippet.py" in diff_patch
    assert len(summary) > 0
