from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.javascript_analyzer import JavaScriptAnalyzer
from app.schemas.error_model import ErrorCategory, SeverityLevel

def test_python_syntax_error():
    analyzer = PythonAnalyzer()
    code = "def foo(\n    print('broken syntax')"
    results = analyzer.analyze(code, "test.py")
    assert len(results) > 0
    assert results[0].category == ErrorCategory.SYNTAX
    assert results[0].severity == SeverityLevel.CRITICAL

def test_python_predictive_index_error():
    analyzer = PythonAnalyzer()
    code = "items = [10, 20, 30]\nval = items[5]"
    results = analyzer.analyze(code, "test.py")
    assert any(r.rule_id == "PRED-001" for r in results)

def test_python_security_secret_detection():
    analyzer = PythonAnalyzer()
    code = 'API_KEY = "sk-1234567890abcdef12345678"'
    results = analyzer.analyze(code, "test.py")
    assert any(r.category == ErrorCategory.SECURITY for r in results)

def test_python_performance_nested_loops():
    analyzer = PythonAnalyzer()
    code = "for i in range(10):\n    for j in range(10):\n        for k in range(10):\n            print(i, j, k)"
    results = analyzer.analyze(code, "test.py")
    assert any(r.category == ErrorCategory.PERFORMANCE for r in results)

def test_javascript_analyzer():
    analyzer = JavaScriptAnalyzer()
    code = "const val = null.name;"
    results = analyzer.analyze(code, "test.js")
    assert any(r.category == ErrorCategory.TYPE for r in results)
