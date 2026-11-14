from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_problems_seeded():
    res = client.get("/api/problems?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 700
    assert len(data["items"]) == 10


def test_filter_coding_and_aptitude():
    coding = client.get("/api/problems?category=Coding&difficulty=Easy").json()
    aptitude = client.get("/api/problems?category=Aptitude&difficulty=Hard").json()
    assert coding["total"] > 0
    assert aptitude["total"] > 0


def test_auth_register_and_login():
    email = "ci_test_student@vtu.edu"
    client.post("/api/auth/register", json={
        "name": "CI Test Student",
        "email": email,
        "password": "password123",
        "targetRole": "Software Engineer"
    })
    login_res = client.post("/api/auth/login", json={
        "email": email,
        "password": "password123"
    })
    assert login_res.status_code == 200
    assert login_res.json()["user"]["email"] == email


def test_python_code_submission_all_cases():
    code = """
def solve(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n] + i
        seen[n] = i
    return -1
"""
    res = client.post("/api/problems/1/submit", json={
        "userEmail": "ci_test_student@vtu.edu",
        "language": "python",
        "answer": code,
        "timeTakenSec": 45
    })
    assert res.status_code == 200
    data = res.json()
    assert data["allPassed"] is True
    assert data["passedCases"] == data["totalCases"]


def test_ai_mock_interview():
    res = client.post("/api/ai/coach", json={
        "userEmail": "ci_test_student@vtu.edu",
        "roundType": "MockInterview",
        "userMessage": "Start interview",
        "history": [],
        "targetRole": "Software Engineer"
    })
    assert res.status_code == 200
    assert "reply" in res.json()