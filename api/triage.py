from typing import get_args

from botocore.config import Config
from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel, Field

from api.models import Category, Severity, Ticket

MODEL_ID = "eu.amazon.nova-micro-v1:0"
REGION = "eu-north-1"

CATEGORIES = ", ".join(get_args(Category))
SEVERITIES = ", ".join(get_args(Severity))

config = Config(
    connect_timeout=15,
    read_timeout=30,
    retries={"max_attempts": 3, "mode": "standard"},
)


class TriageResult(BaseModel):
    category: Category
    severity: Severity
    confidence: float = Field(..., ge=0, le=1)

def build_triage_runnable():
    llm = ChatBedrockConverse(model= MODEL_ID, region_name= REGION, temperature=0, config=config)
    return llm.with_structured_output(TriageResult)

def triage_ticket(ticket: Ticket, runnable) -> TriageResult:
    prompt = f"""
    You are a triage assistant for IT support tickets.
    The ticket has the following description: {ticket.description}
    Please classify it into one of the following categories: {CATEGORIES}
    And assign it one of the following severities: {SEVERITIES}
    Confidence should be a float between 0 and 1,
    indicating how confident you are in your classification.
    """
    return runnable.invoke(prompt)