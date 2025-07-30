import requests

BASE_URL = "http://192.168.58.2:31837"

def test_root():
    res = requests.get(BASE_URL + "/")
    assert res.status_code == 200
    assert res.json()["message"] == "Billing Service is running"

def test_charge():
    res = requests.post(f"{BASE_URL}/charge", json={"username": "Alice"})
    assert res.status_code == 200
    assert "User 'Alice' charged successfully" in res.json()["message"]

def test_metrics():
    res = requests.get(f"{BASE_URL}/metrics")
    assert res.status_code == 200
