from typing import Any

from app.models import ToolResult
from app.tools import (
    ApiMetricsTool,
    DatabaseInspectionTool,
    ErrorFrequencyTool,
    RecentDeploymentsTool,
    SearchLogsTool,
    ServiceHealthTool,
)


TOOLS = {
    "get_error_frequency": ErrorFrequencyTool(),
    "search_logs": SearchLogsTool(),
    "get_recent_deployments": RecentDeploymentsTool(),
    "get_service_health": ServiceHealthTool(),
    "get_api_metrics": ApiMetricsTool(),
    "inspect_database": DatabaseInspectionTool(),
}


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> ToolResult:
    tool = TOOLS.get(tool_name)

    if tool is None:
        return ToolResult(
            tool_name=tool_name,
            success=False,
            error=f"Unknown tool: {tool_name}",
        )

    try:
        result = tool.execute(**arguments)

        return ToolResult(
            tool_name=tool_name,
            success=True,
            data=result,
        )

    except Exception as exc:
        return ToolResult(
            tool_name=tool_name,
            success=False,
            error=str(exc),
        )