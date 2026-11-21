# graph/state.py
# one comment per field: which node WRITES it, and overwrite or append
import operator
from typing import Annotated, TypedDict

from pydantic import BaseModel, Field

from api.models import Ticket
from api.triage import TriageResult


class Resolution(BaseModel):
    steps: list[str]                 # the fix, step by step
    cited_runbook_ids: list[str]     # which runbooks the steps came from
    confidence: float = Field(ge=0, le=1)


class TicketState(TypedDict):
    ticket: Ticket                      #the caller at invoke, overwrite.
    triage: TriageResult | None         #triage_ticket, overwrite, no reducer	
    retrieved_chunks: list[str] | None  #retreive(), overwrite
    resolution: Resolution | None       #resolve node, overwrite, no reducer	
    needs_human: bool #triage on low confidence or severity 1,overwrite, no reducer	
    error: Annotated[list[str], operator.add] #any node that catches an exception; starts as [],
    #append, with a reducer