import json

from api.main import get_runnable
from api.models import Ticket
from api.triage import triage_ticket

items = json.load(open("tests/data/sample_tickets.json", encoding="utf-8"))
runnable = get_runnable()
correct = 0
parse_failures = 0
for item in items:
    ticket = Ticket(**item)  # Ticket requires category; triage_ticket only uses the description
    try:
        result = triage_ticket(ticket, runnable=runnable)
    except ValueError:  # bad JSON or failed TriageResult validation
        parse_failures += 1
        continue
    if result.category == item["category"]:
        correct += 1
print(f"baseline: {correct}/{len(items)} category accuracy, {parse_failures} parse failures")