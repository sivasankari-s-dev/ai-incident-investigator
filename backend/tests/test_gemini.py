import os

import pytest

from app.agent.tool_definitions import TOOL_DEFINITIONS
from app.services.llm import GeminiService


@pytest.mark.integration
def test_gemini_tool_call():
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY is not configured")

    llm = GeminiService()

    response = llm.generate(
        """
        You are investigating an incident affecting the payment-api.

        The payment API is reporting failures.

        Determine the first useful investigation action.
        Use one of the available tools.
        """,
        tools=TOOL_DEFINITIONS,
    )

    assert response.candidates
    assert response.candidates[0].content.parts
    