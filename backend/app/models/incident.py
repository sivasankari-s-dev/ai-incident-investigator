from datetime import datetime

from pydantic import BaseModel, Field


class Incident(BaseModel):
    title: str
    description: str
    service: str
    severity: str
    reported_at: datetime


class Evidence(BaseModel):
    source: str
    observation: str
    timestamp: datetime | None = None
    relevance: str | None = None


class Hypothesis(BaseModel):
    description: str
    supporting_evidence: list[str] = Field(default_factory=list)
    contradicting_evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    status: str = "unconfirmed"