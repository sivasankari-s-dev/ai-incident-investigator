import json
from pathlib import Path
from typing import Any

from app.tools.base import InvestigationTool


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "metrics.json"


class ApiMetricsTool(InvestigationTool):
    name = "get_api_metrics"
    description = "Get API operational metrics for a service."

    def execute(
        self,
        service: str,
        metric: str | None = None,
    ) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            metrics = json.load(file)

        results = [
            item for item in metrics
            if item["service"] == service
        ]

        if metric:
            allowed_metrics = {
                "request_count",
                "error_count",
                "error_rate",
                "latency_ms",
            }

            if metric not in allowed_metrics:
                return {
                    "error": f"Unsupported metric: {metric}"
                }

            results = [
                {
                    "timestamp": item["timestamp"],
                    "service": item["service"],
                    metric: item[metric],
                }
                for item in results
            ]

        return {
            "service": service,
            "metrics": results,
        }


class ErrorFrequencyTool(InvestigationTool):
    name = "get_error_frequency"
    description = "Get error frequency for a service."

    def execute(self, service: str) -> dict[str, Any]:
        with DATA_FILE.open() as file:
            metrics = json.load(file)

        results = [
            item for item in metrics
            if item["service"] == service
        ]

        if not results:
            return {
                "service": service,
                "error_count": 0,
                "error_rate": 0,
            }

        latest = results[-1]

        return {
            "service": service,
            "timestamp": latest["timestamp"],
            "error_count": latest["error_count"],
            "error_rate": latest["error_rate"],
        }