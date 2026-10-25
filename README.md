# IT Incident Triage & Resolution Agent

An AI agent that reads an incoming IT support ticket, classifies its category and
severity, retrieves matching runbooks from a knowledge base (RAG), and proposes
resolution steps. Built with FastAPI, LangGraph and AWS Bedrock, with evaluation
and failure tracking from day one.

## Architecture
_TODO: diagram goes here (Wk5+)._

Planned flow: Ticket → API (FastAPI) → Graph (LangGraph: classify → retrieve → propose) → RAG (runbooks) → Response

## Run it
```
uv run fastapi dev api/main.py
```
Needs AWS credentials with Bedrock access (region `eu-north-1`, model `eu.amazon.nova-micro-v1:0`).

Example request (PowerShell; use `curl.exe`, plain `curl` is an alias, and put the body in a file to avoid quote escaping):
```
curl.exe -X POST http://127.0.0.1:8000/tickets -H "Content-Type: application/json" --data-binary "@ticket.json"
```
where `ticket.json` is:
```json
{"ticket_id": "T-900", "description": "VPN drops every 10 minutes", "category": "network", "severity": "high", "created_at": "2026-10-01T09:30:00"}
```
Real response: `{"category":"network","severity":"high","confidence":0.95}`

## How a request flows
The JSON body is validated into a Pydantic `Ticket`; a bad body (missing field, empty description, wrong type) is rejected by FastAPI with **422** before any model call. `triage_ticket` builds a prompt from the description and calls Bedrock `converse`. The reply text is parsed as JSON and validated into a `TriageResult` (category and severity are `Literal` values, confidence is 0 to 1), and that is returned as JSON. If the model's text is not valid JSON or fails validation, the route returns **502**; if Bedrock itself fails (`ClientError`: throttling, access, network), it returns **503**. Every request writes one log line with `request_id`, `status`, `latency_ms` and token counts (never the ticket text or model output).

## Baseline
First run of `uv run python -m scripts.run_baseline` on the 20 tickets in `tests/data/sample_tickets.json` (single run, no retries):

`baseline: 18/20 category accuracy, 0 parse failures`

`structured-output baseline: 17/20 category accuracy, 0 parse failures (LangChain with_structured_output, Nova Micro, 25 Oct)`

Note: pytest uses a fake Bedrock client, so it proves plumbing, not model behaviour.

## Folders
- `api/` – FastAPI app and Pydantic models
- `graph/` – LangGraph workflow
- `rag/` – retrieval over runbooks
- `tests/` – pytest suite

## Failure journal
See [FAILURES.md](FAILURES.md).