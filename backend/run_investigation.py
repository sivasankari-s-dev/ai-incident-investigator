from datetime import datetime

from app.agent import IncidentInvestigator
from app.models import Incident, InvestigationState


incident = Incident(
    title="Payment API failures",
    description="The Payment API started returning a large number of HTTP 500 errors.",
    service="payment-api",
    severity="high",
    reported_at=datetime(2026, 8, 25, 10, 15),
)

state = InvestigationState(
    incident=incident,
)

investigator = IncidentInvestigator()

result = investigator.investigate(state)

print("\nSTATUS:", result.status)
print("ITERATIONS:", result.iteration)
print("TOOL CALLS:", len(result.tool_calls))

for call in result.tool_calls:
    print(
        f"- {call.tool_name}({call.arguments})"
    )

print("\nFINAL REPORT:")
print(result.final_report.model_dump_json(indent=2))