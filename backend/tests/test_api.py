from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Code Doctor" in response.json()["name"]

def test_api_analyze():
    payload = {
        "code": "items = [10, 20]\nprint(items[5])",
        "language": "python",
        "learning_level": "Beginner"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_issues"] > 0
    assert "health_score" in data

def test_api_fix():
    payload = {
        "code": "API_KEY = 'sk-1234567890abcdef12345678'",
        "issue_id": "SEC-SECRET-1",
        "rule_id": "SEC-001",
        "line": 1
    }
    response = client.post("/api/v1/fix", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "patched_code" in data
    assert "diff_patch" in data

def test_api_verify():
    payload = {
        "original_code": "API_KEY = 'sk-1234567890abcdef12345678'",
        "patched_code": "import os\nAPI_KEY = os.getenv('API_KEY', '')",
        "rule_id": "SEC-001"
    }
    response = client.post("/api/v1/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is True

def test_api_platforms():
    response = client.get("/api/v1/platforms")
    assert response.status_code == 200
    platforms = response.json()
    assert len(platforms) >= 5

def test_api_languages():
    response = client.get("/api/v1/languages")
    assert response.status_code == 200
    langs = response.json()
    assert len(langs) >= 3
