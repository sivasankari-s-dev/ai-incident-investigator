from __future__ import annotations
from enum import Enum

from pydantic import BaseModel, Field

from app.models.incident import Evidence, Hypothesis, Incident
from app.models.tool import ToolCall, ToolResult


class InvestigationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"
    FAILED = "failed"


class InvestigationState(BaseModel):
    incident: Incident
    status: InvestigationStatus = InvestigationStatus.PENDING
    observations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    current_hypothesis: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    next_action: str | None = None
    iteration: int = 0
    final_report: "InvestigationReport | None" = None


class RecommendedAction(BaseModel):
    action: str
    priority: str


class InvestigationReport(BaseModel):
    summary: str
    root_cause: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: list[Evidence] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    conclusion: str