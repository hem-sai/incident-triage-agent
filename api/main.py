import boto3
from botocore.exceptions import ClientError
from fastapi import Depends, FastAPI, HTTPException

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
    try:
        return triage_ticket(ticket, client)
    except ClientError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except ValueError:
        # Safe to catch broadly: triage_ticket only raises ValueError from the parse/validate step.
        raise HTTPException(status_code=502, detail="Bad gateway")