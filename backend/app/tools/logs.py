import json
from pathlib import Path
from typing import Any

from app.tools.base import InvestigationTool


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "logs.json"


class SearchLogsTool(InvestigationTool):
    name = "search_logs"
    description = "Search application logs by service, level, and keyword."

    def execute(
        self,
        service: str | None = None,
        level: str | None = None,
        keyword: str | None = None,
    ) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            logs = json.load(file)

        results = logs

        if service:
            results = [
                log for log in results
                if log["service"] == service
            ]

        if level:
            results = [
                log for log in results
                if log["level"] == level
            ]

        if keyword:
            keyword_lower = keyword.lower()
            results = [
                log for log in results
                if keyword_lower in log["message"].lower()
            ]

        return {
            "count": len(results),
            "logs": results,
        }