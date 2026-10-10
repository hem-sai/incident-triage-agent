from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Severity = Literal["low", "medium", "high", "critical"]
Category = Literal["network", "access", "hardware", "software", "email"]
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Ticket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(pattern=r"^T-\d{3,}$")
    description: NonEmptyStr
    category: Category
    severity: Severity
    created_at: datetime


class Runbook(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runbook_id: str = Field(pattern=r"^RB-\d{3,}$")
    title: NonEmptyStr
    steps: list[NonEmptyStr] = Field(min_length=1)
    applicable_categories: list[Category] = Field(min_length=1)