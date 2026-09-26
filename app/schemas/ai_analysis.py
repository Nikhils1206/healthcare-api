from typing import Literal

from pydantic import BaseModel, Field


class AIClaimAnalysis(BaseModel):
    risk_score: float = Field(ge=0, le=1)
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    flags: list[str]
    summary: str