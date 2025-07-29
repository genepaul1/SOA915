import requests

BASE_URL = "http://192.168.58.2:30628"

def test_health_check():
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200

def test_send_notification():
    data = {
        "email": "notify@example.com",
        "message": "Test message"
    }
    response = requests.post(BASE_URL + "/notify", json=data)
    assert response.status_code == 200

def test_metrics():
    response = requests.get(BASE_URL + "/metrics")
    assert response.status_code == 200
