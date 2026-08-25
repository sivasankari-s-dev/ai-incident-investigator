from app.tools import (
    ApiMetricsTool,
    DatabaseInspectionTool,
    ErrorFrequencyTool,
    RecentDeploymentsTool,
    SearchLogsTool,
    ServiceHealthTool,
)


def test_search_logs():
    tool = SearchLogsTool()

    result = tool.execute(
        service="payment-api",
        level="ERROR",
        keyword="database",
    )

    assert result["count"] > 0
    assert all(log["level"] == "ERROR" for log in result["logs"])


def test_recent_deployments():
    tool = RecentDeploymentsTool()

    result = tool.execute(
        service="payment-api",
        minutes=60,
    )

    assert len(result["deployments"]) > 0
    assert any(
        deployment["version"] == "v2.4.1"
        for deployment in result["deployments"]
    )


def test_api_metrics():
    tool = ApiMetricsTool()

    result = tool.execute(
        service="payment-api",
        metric="error_rate",
    )

    assert len(result["metrics"]) > 0
    assert result["metrics"][-1]["error_rate"] > 0.5


def test_error_frequency():
    tool = ErrorFrequencyTool()

    result = tool.execute(service="payment-api")

    assert result["error_count"] > 0
    assert result["error_rate"] > 0


def test_service_health():
    tool = ServiceHealthTool()

    result = tool.execute(service="payment-api")

    assert result["status"] == "degraded"
    assert result["dependencies"]["database"] == "unhealthy"


def test_database_inspection():
    tool = DatabaseInspectionTool()

    result = tool.execute(service="payment-api")

    database = result["database_status"]

    assert database is not None
    assert database["connection_pool"]["utilization_percent"] == 100
    