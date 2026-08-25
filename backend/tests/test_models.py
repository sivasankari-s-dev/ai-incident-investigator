from datetime import datetime

from app.models import (
    Evidence,
    Incident,
    InvestigationState,
    InvestigationStatus,
)


def test_incident_model():
    incident = Incident(
        title="Payment API failures",
        description="Payment API is returning HTTP 500 errors.",
        service="payment-api",
        severity="high",
        reported_at=datetime(2026, 8, 25, 10, 15),
    )

    assert incident.service == "payment-api"
    assert incident.severity == "high"


def test_investigation_state_defaults():
    incident = Incident(
        title="Payment API failures",
        description="Payment API is returning HTTP 500 errors.",
        service="payment-api",
        severity="high",
        reported_at=datetime(2026, 8, 25, 10, 15),
    )

    state = InvestigationState(incident=incident)

    assert state.status == InvestigationStatus.PENDING
    assert state.iteration == 0
    assert state.evidence == []
    assert state.hypotheses == []
    assert state.tool_calls == []
    assert state.tool_results == []


def test_evidence_model():
    evidence = Evidence(
        source="database",
        observation="Connection pool is at 100% utilization.",
        timestamp=datetime(2026, 8, 25, 10, 10),
        relevance="Supports database connection exhaustion hypothesis.",
    )

    assert evidence.source == "database"
    assert evidence.timestamp is not None