import json
from pathlib import Path
from typing import Any

from app.tools.base import InvestigationTool


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "database.json"


class DatabaseInspectionTool(InvestigationTool):
    name = "inspect_database"
    description = "Inspect database connection pool and connection errors."

    def execute(self, service: str) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            database_data = json.load(file)

        results = [
            item
            for item in database_data
            if item["service"] == service
        ]

        return {
            "service": service,
            "database_status": results[-1] if results else None,
        }