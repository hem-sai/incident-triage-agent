# IT Incident Triage & Resolution Agent

An AI agent that reads an incoming IT support ticket, classifies its category and
severity, retrieves matching runbooks from a knowledge base (RAG), and proposes
resolution steps. Built with FastAPI, LangGraph and AWS Bedrock, with evaluation
and failure tracking from day one.

## Architecture
_TODO: diagram goes here (Wk5+)._

Planned flow: Ticket → API (FastAPI) → Graph (LangGraph: classify → retrieve → propose) → RAG (runbooks) → Response

## Folders
- `api/` – FastAPI app and Pydantic models
- `graph/` – LangGraph workflow
- `rag/` – retrieval over runbooks
- `tests/` – pytest suite

## Failure journal
See [FAILURES.md](FAILURES.md).