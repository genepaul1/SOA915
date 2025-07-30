import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_health_check():
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.json()

def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200
