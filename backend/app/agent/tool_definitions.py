from google.genai import types


TOOL_DEFINITIONS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_error_frequency",
                description="Get the latest error frequency for a service.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service.",
                        ),
                    },
                    required=["service"],
                ),
            ),
            types.FunctionDeclaration(
                name="search_logs",
                description="Search application logs by service, log level, and keyword.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service.",
                        ),
                        "level": types.Schema(
                            type=types.Type.STRING,
                            description="Log level such as INFO, WARNING, or ERROR.",
                        ),
                        "keyword": types.Schema(
                            type=types.Type.STRING,
                            description="Keyword to search for in log messages.",
                        ),
                    },
                    required=["service"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_recent_deployments",
                description="Get recent deployments for a service.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service.",
                        ),
                        "minutes": types.Schema(
                            type=types.Type.INTEGER,
                            description="Lookback window in minutes.",
                        ),
                    },
                    required=["service"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_service_health",
                description="Get service health and dependency health.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service.",
                        ),
                    },
                    required=["service"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_api_metrics",
                description="Get API operational metrics for a service.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service.",
                        ),
                        "metric": types.Schema(
                            type=types.Type.STRING,
                            description="Metric such as error_rate, error_count, latency_ms, or request_count.",
                        ),
                    },
                    required=["service"],
                ),
            ),
            types.FunctionDeclaration(
                name="inspect_database",
                description="Inspect database connection pool state and connection errors.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "service": types.Schema(
                            type=types.Type.STRING,
                            description="Name of the service using the database.",
                        ),
                    },
                    required=["service"],
                ),
            ),
        ]
    )
]