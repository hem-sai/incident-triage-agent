import logging
import time
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from fastapi import Depends, FastAPI, HTTPException

from api.models import Ticket
from api.triage import TriageResult, triage_ticket

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("triage")

app = FastAPI()

config = Config(
    connect_timeout=60,
    read_timeout=60,
    retries={"max_attempts": 3, "mode": "standard"},
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name="eu-north-1", config=config)


@app.post("/tickets")
def create_ticket(ticket: Ticket, client=Depends(get_bedrock_client)) -> TriageResult:
    request_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()
    status = "500"
    usage: dict = {}
    try:
        result, usage =  triage_ticket(ticket, client)
        status = "200"
        return result
    except ClientError:
        status = "503"
        raise HTTPException(status_code=503, detail="Service unavailable")
    except ValueError:
        # Safe to catch broadly: triage_ticket only raises ValueError from the parse/validate step.
        status = "502"
        raise HTTPException(status_code=502, detail="Bad gateway")
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
        "request_id=%s status=%s latency_ms=%.1f input_tokens=%s output_tokens=%s",
        request_id, status, elapsed_ms,
        usage.get("inputTokens", 0), usage.get("outputTokens", 0),
        )
