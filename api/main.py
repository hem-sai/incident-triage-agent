from fastapi import FastAPI

from api.models import Ticket

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tickets")
def create_ticket(ticket: Ticket) -> Ticket:
    return ticket
