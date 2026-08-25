import json
from typing import Any

from google.genai import types

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tool_definitions import TOOL_DEFINITIONS
from app.agent.tool_registry import execute_tool
from app.models import (
    Evidence,
    InvestigationReport,
    InvestigationState,
    RecommendedAction,
    ToolCall,
)
from app.services.llm import GeminiService


MAX_ITERATIONS = 8
MAX_TOOL_CALLS = 12


class IncidentInvestigator:
    def __init__(
        self,
        llm: GeminiService | None = None,
    ) -> None:
        self.llm = llm or GeminiService()

    def investigate(
        self,
        state: InvestigationState,
    ) -> InvestigationState:
        state.status = "running"

        contents: list[Any] = [
            SYSTEM_PROMPT,
            self._build_incident_prompt(state),
        ]

        total_tool_calls = 0

        for iteration in range(1, MAX_ITERATIONS + 1):
            state.iteration = iteration

            response = self.llm.generate(
                contents=contents,
                tools=TOOL_DEFINITIONS,
            )

            candidate = response.candidates[0]
            model_content = candidate.content

            contents.append(model_content)

            function_calls = [
                part.function_call
                for part in model_content.parts
                if part.function_call
            ]

            if not function_calls:
                report = self._build_final_report(
                    state,
                    model_content,
                )

                state.final_report = report
                state.confidence = report.confidence

                if report.root_cause:
                    state.status = "completed"
                else:
                    state.status = "inconclusive"

                return state

            function_response_parts = []

            for function_call in function_calls:
                if total_tool_calls >= MAX_TOOL_CALLS:
                    state.status = "inconclusive"
                    state.final_report = self._inconclusive_report(
                        "Investigation tool-call budget exhausted."
                    )
                    return state

                tool_name = function_call.name
                arguments = dict(function_call.args or {})

                state.tool_calls.append(
                    ToolCall(
                        tool_name=tool_name,
                        arguments=arguments,
                    )
                )

                result = execute_tool(
                    tool_name,
                    arguments,
                )

                state.tool_results.append(result)
                total_tool_calls += 1

                if result.success:
                    state.observations.append(
                        f"{tool_name}: {json.dumps(result.data)}"
                    )
                else:
                    state.observations.append(
                        f"{tool_name} failed: {result.error}"
                    )

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=tool_name,
                        response={
                            "success": result.success,
                            "data": result.data,
                            "error": result.error,
                        },
                    )
                )

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        state.status = "inconclusive"
        state.final_report = self._inconclusive_report(
            "Investigation iteration limit exhausted."
        )

        return state

    def _build_incident_prompt(
        self,
        state: InvestigationState,
    ) -> str:
        incident = state.incident

        return f"""
Incident:

Title: {incident.title}
Description: {incident.description}
Service: {incident.service}
Severity: {incident.severity}
Reported at: {incident.reported_at.isoformat()}

Begin the investigation.

Choose the most useful next investigation action.
"""

    # def _build_final_report(
    #     self,
    #     state: InvestigationState,
    #     model_content: Any,
    # ) -> InvestigationReport:
    #     text_parts = [
    #         part.text
    #         for part in model_content.parts
    #         if part.text
    #     ]

    #     text = "\n".join(text_parts).strip()

    #     return InvestigationReport(
    #         summary=text or "Investigation completed.",
    #         root_cause=text or None,
    #         confidence=state.confidence,
    #         evidence=[],
    #         recommended_actions=[],
    #         conclusion=text or "Investigation completed.",
    #     )

    # def _build_final_report(
    #     self,
    #     state: InvestigationState,
    #     model_content: Any,
    # ) -> InvestigationReport:
    #     text_parts = [
    #         part.text
    #         for part in model_content.parts
    #         if part.text
    #     ]

    #     text = "\n".join(text_parts).strip()

    #     evidence = []

    #     for result in state.tool_results:
    #         if result.success:
    #             evidence.append(
    #                 Evidence(
    #                     source=result.tool_name,
    #                     observation=json.dumps(
    #                         result.data,
    #                         default=str,
    #                     ),
    #                 )
    #             )

    #     return InvestigationReport(
    #         summary=text or "Investigation completed.",
    #         root_cause=text or None,
    #         confidence=state.confidence,
    #         evidence=evidence,
    #         recommended_actions=[],
    #         conclusion=text or "Investigation completed.",
    #     )

    def _build_final_report(
        self,
        state: InvestigationState,
        model_content: Any,
    ) -> InvestigationReport:
        investigation_summary = "\n".join(
            state.observations
        )

        prompt = f"""
    You are producing the final report for an incident investigation.

    Incident:
    {state.incident.model_dump_json(indent=2)}

    Investigation evidence:
    {investigation_summary}

    Tool results:
    {json.dumps(
        [
            {
                "tool": result.tool_name,
                "success": result.success,
                "data": result.data,
            }
            for result in state.tool_results
        ],
        indent=2,
        default=str,
    )}

    Produce a structured investigation report.

    Requirements:

    1. summary:
    Briefly summarize what happened.

    2. root_cause:
    State the most strongly supported root cause.
    If the evidence is insufficient, use null.

    3. confidence:
    A number between 0 and 1 representing confidence in the root cause.

    4. evidence:
    List only evidence directly supported by the tool results.

    5. recommended_actions:
    Provide concrete actions that an operator should take.

    6. conclusion:
    State whether the root cause is confirmed, probable, or inconclusive.

    Do not invent evidence.
    Do not treat a hypothesis as confirmed unless the evidence supports it.
    """

        response = self.llm.generate_structured(
            contents=prompt,
            response_schema=InvestigationReport,
        )

        parsed = response.parsed

        if parsed is None:
            raise ValueError(
                "Gemini returned no structured investigation report"
            )

        return parsed
        

    def _inconclusive_report(
        self,
        reason: str,
    ) -> InvestigationReport:
        return InvestigationReport(
            summary="The investigation could not establish a sufficiently supported root cause.",
            root_cause=None,
            confidence=0.0,
            evidence=[],
            recommended_actions=[
                RecommendedAction(
                    action="Review the available incident evidence manually.",
                    priority="high",
                )
            ],
            conclusion=reason,
        )