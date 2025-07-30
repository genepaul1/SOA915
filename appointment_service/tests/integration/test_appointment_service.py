import requests

BASE_URL = "http://192.168.58.2:30002"

def test_index():
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    assert "message" in res.json()

def test_book_appointment():
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "date": "2025-08-01",
        "time": "10:00"
    }
    res = requests.post(f"{BASE_URL}/book", json=payload)
    assert res.status_code == 200
    assert "message" in res.json()

def test_get_appointments():
    res = requests.get(f"{BASE_URL}/appointments")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_metrics():
    res = requests.get(f"{BASE_URL}/metrics")
    assert res.status_code == 200
