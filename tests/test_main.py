#!/usr/bin/python3
"""Test module for the main application"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
