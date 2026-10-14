import json
from typing import get_args

from pydantic import BaseModel, Field

from api.models import Category, Severity, Ticket

MODEL_ID = "eu.amazon.nova-micro-v1:0"

CATEGORIES = ", ".join(get_args(Category))
SEVERITIES = ", ".join(get_args(Severity))


class TriageResult(BaseModel):
    category: Category
    severity: Severity
    confidence: float = Field(..., ge=0, le=1)


def triage_ticket(ticket: Ticket, client) -> TriageResult:
    prompt = f"""
    You are a triage assistant for IT support tickets.
    The ticket has the following description: {ticket.description}
    Please classify it into one of the following categories: {CATEGORIES}
    And assign it one of the following severities: {SEVERITIES}
    Confidence should be a float between 0 and 1,
    indicating how confident you are in your classification.
    Reply with JSON only, containing the keys 'category', 'severity', and 'confidence'.
    """
    response = client.converse(
        modelId=MODEL_ID, messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    text = response["output"]["message"]["content"][0]["text"]
    data = json.loads(text)
    return TriageResult.model_validate(data)
