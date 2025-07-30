import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from flask import json
from main import app

client = app.test_client()

def test_index():
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()

def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200
