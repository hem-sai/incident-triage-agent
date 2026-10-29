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
The JSON body is validated into a Pydantic `Ticket`; a bad body (missing field, empty description, wrong type) is rejected by FastAPI with **422** before any model call. `triage_ticket` sends the description to Bedrock Nova Micro through LangChain `ChatBedrockConverse.with_structured_output(TriageResult)`, which returns a validated `TriageResult` (category and severity are `Literal` values, confidence is 0 to 1). If the output cannot be parsed or fails validation (`ValueError`), the route returns **502**. If the Bedrock call fails (`ClientError` such as throttling or access, or `BotoCoreError` such as read and connect timeouts), it returns **503**. Every request writes one log line with `request_id`, `status` and `latency_ms` (never the ticket text or model output). Token counts are logged as 0 for now because structured output drops the usage data (see `TODO.md`).

## Baseline
Command: `uv run python -m scripts.run_baseline` on the 20 tickets in `tests/data/sample_tickets.json`. Every row is a single run, no retries, Nova Micro, temperature 0.

| Date | Method | Category accuracy | Parse failures |
|------|--------|-------------------|----------------|
| 16 Oct | Raw Bedrock `converse`, JSON parsed by hand | 18/20 | 0 |
| 25 Oct | LangChain `with_structured_output` | 17/20 | 0 |
| 28 Oct | LangChain `with_structured_output` (same code) | 20/20 | 0 |

The 25 Oct and 28 Oct runs use the same code, model and temperature, and the score moved by 3 tickets. So the baseline is noisy: on 20 tickets one ticket is 5 points, and a single run cannot show that one setup beats another. Do not claim a method change moved accuracy until the same setup is run several times or tested on the 30-question golden set.

Note: pytest uses a fake Bedrock client, so it proves plumbing, not model behaviour.

## Retrieval index
`uv run python -m rag.index` loads the 30 runbooks in `rag/runbooks/`, splits them with `RecursiveCharacterTextSplitter`, embeds the chunks with Titan Text Embeddings V2 (`amazon.titan-embed-text-v2:0`) through `BedrockEmbeddings`, and stores them in an `InMemoryVectorStore`. Titan v2 is available in `eu-north-1`, the same region as the Nova calls, so no other region is needed. Each chunk keeps its `runbook_id` (the file name) in metadata. `build_index(chunk_size, chunk_overlap)` takes both settings as parameters. The index is rebuilt on every run and lost when the process exits (a learning shortcut; production would use a persistent store). One runbook can return several chunks in the top hits, so `retrieve` has to dedupe by `runbook_id`.

## Folders
- `api/` – FastAPI app and Pydantic models
- `graph/` – LangGraph workflow
- `rag/` – retrieval over runbooks
- `tests/` – pytest suite

## Failure journal
See [FAILURES.md](FAILURES.md).