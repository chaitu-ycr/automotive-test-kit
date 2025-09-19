import pytest
from fastapi.testclient import TestClient
from src.py_uds_demo.interface.api import app

client = TestClient(app)

def test_send_request():
    response = client.post("/send_request", json={"data": [0x22, 0xF1, 0x87]})
    assert response.status_code == 200
    assert "response" in response.json()

def test_get_help_found():
    response = client.get("/help/16")  # 0x10
    assert response.status_code == 200
    assert "docstring" in response.json()

def test_get_help_not_found():
    response = client.get("/help/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "No help found for SID 0x63"
