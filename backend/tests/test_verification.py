from app.core.verification import FixVerificationEngine

def test_fix_verification_pass():
    original_code = "API_KEY = 'sk-1234567890abcdef12345678'"
    patched_code = "import os\nAPI_KEY = os.getenv('API_KEY', '')"

    res = FixVerificationEngine.verify_patch(original_code, patched_code, language="python", rule_id="SEC-001")
    assert res.passed is True
    assert res.status == "VERIFIED"

def test_fix_verification_reject_syntax_error():
    original_code = "x = 10"
    patched_code = "x = (def broken syntax"

    res = FixVerificationEngine.verify_patch(original_code, patched_code, language="python")
    assert res.passed is False
    assert res.status == "REJECTED"
