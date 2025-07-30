import requests

BASE_URL = "http://192.168.58.2:32680"

def test_health_check():
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    assert "message" in res.json()

def test_register_user():
    payload = {
        "username": "alice123",
        "email": "alice123@example.com"
    }
    res = requests.post(f"{BASE_URL}/register", json=payload)
    assert res.status_code in [200, 400]
    assert "message" in res.json() or "detail" in res.json()

def test_list_users():
    res = requests.get(f"{BASE_URL}/users")
    assert res.status_code == 200
    assert "users" in res.json()

def test_metrics():
    res = requests.get(f"{BASE_URL}/metrics")
    assert res.status_code == 200
