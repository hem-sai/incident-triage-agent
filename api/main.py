import logging
import time
import uuid

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import Depends, FastAPI, HTTPException

from api.models import Ticket
from api.triage import TriageResult, build_triage_runnable, triage_ticket

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("triage")

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

def get_runnable():
    return build_triage_runnable()


@app.post("/tickets")
def create_ticket(ticket: Ticket, runnable=Depends(get_runnable)) -> TriageResult:
    request_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()
    status = "500"
    usage: dict = {}
    try:
        result =  triage_ticket(ticket, runnable=runnable)
        status = "200"
        return result
    except (ClientError, BotoCoreError):
        # ReadTimeoutError / ConnectTimeoutError derive from BotoCoreError, not ClientError.
        status = "503"
        raise HTTPException(status_code=503, detail="Service unavailable")
    except ValueError:
        # pydantic ValidationError and LangChain OutputParserException both subclass ValueError
        status = "502"
        raise HTTPException(status_code=502, detail="Bad gateway")
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
        "request_id=%s status=%s latency_ms=%.1f input_tokens=%s output_tokens=%s",
        request_id, status, elapsed_ms,
        usage.get("inputTokens", 0), usage.get("outputTokens", 0),
        )
