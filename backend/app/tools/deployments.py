import json
from pathlib import Path
from typing import Any

from app.tools.base import InvestigationTool


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "deployments.json"


class RecentDeploymentsTool(InvestigationTool):
    name = "get_recent_deployments"
    description = "Get recent deployments for a service."

    def execute(
        self,
        service: str,
        minutes: int = 60,
    ) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            deployments = json.load(file)

        service_deployments = [
            deployment
            for deployment in deployments
            if deployment["service"] == service
        ]

        return {
            "service": service,
            "window_minutes": minutes,
            "deployments": service_deployments,
        }