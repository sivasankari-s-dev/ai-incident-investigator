
from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.models import (
    Incident,
    InvestigationState,
    InvestigationStatus,
)


client = TestClient(app)


def valid_incident_payload():
    return {
        "title": "Payment API failures",
        "description": "Payment API is returning HTTP 500 errors.",
        "service": "payment-api",
        "severity": "high",
        "reported_at": "2026-08-25T10:15:00",
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_investigation_success(monkeypatch):
    def fake_investigate(self, state):
        state.status = InvestigationStatus.COMPLETED
        state.iteration = 2
        state.observations.append("Database connection pool exhausted.")
        return state

    monkeypatch.setattr(
        "app.main.IncidentInvestigator.investigate",
        fake_investigate,
    )

    response = client.post(
        "/investigations",
        json=valid_incident_payload(),
    )

    assert response.status_code == 200

    data = response.json()
    assert data["incident"]["service"] == "payment-api"
    assert data["status"] == "completed"
    assert data["iteration"] == 2
    assert "Database connection pool exhausted." in data["observations"]


def test_create_investigation_rejects_invalid_input():
    payload = valid_incident_payload()
    del payload["reported_at"]

    response = client.post("/investigations", json=payload)

    assert response.status_code == 422


def test_create_investigation_handles_agent_failure(monkeypatch):
    def fake_investigate(self, state):
        raise RuntimeError("Simulated investigator failure")

    monkeypatch.setattr(
        "app.main.IncidentInvestigator.investigate",
        fake_investigate,
    )

    response = client.post(
        "/investigations",
        json=valid_incident_payload(),
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Investigation failed."