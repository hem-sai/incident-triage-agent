import boto3
from fastapi import Depends, FastAPI

from api.models import Ticket
from api.triage import TriageResult, triage_ticket

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name="eu-north-1")


@app.post("/tickets")
def create_ticket(ticket: Ticket, client=Depends(get_bedrock_client)) -> TriageResult:
    return triage_ticket(ticket, client)
