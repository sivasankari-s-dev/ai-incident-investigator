import json
from pathlib import Path
from typing import Any

from app.tools.base import InvestigationTool


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "services.json"


class ServiceHealthTool(InvestigationTool):
    name = "get_service_health"
    description = "Get service health and dependency status."

    def execute(self, service: str) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            services = json.load(file)

        for item in services:
            if item["service"] == service:
                return item

        return {
            "service": service,
            "status": "unknown",
            "error": "Service not found",
        }