from datetime import datetime

from app.agent.tool_registry import execute_tool
from app.models import Incident, InvestigationState


def test_tool_registry_executes_known_tool():
    result = execute_tool(
        "get_error_frequency",
        {"service": "payment-api"},
    )

    assert result.success is True
    assert result.data["error_rate"] > 0


def test_tool_registry_rejects_unknown_tool():
    result = execute_tool(
        "unknown_tool",
        {},
    )

    assert result.success is False
    assert "Unknown tool" in result.error


def test_investigation_state_can_be_created():
    incident = Incident(
        title="Payment API failures",
        description="Payment API is returning HTTP 500 errors.",
        service="payment-api",
        severity="high",
        reported_at=datetime(2026, 8, 25, 10, 15),
    )

    state = InvestigationState(
        incident=incident,
    )

    assert state.incident.service == "payment-api"
    assert state.iteration == 0