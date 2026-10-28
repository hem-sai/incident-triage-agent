import json
from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError

from api.models import Ticket
from api.triage import build_triage_runnable, triage_ticket

DATA_PATH = Path(__file__).resolve().parent.parent / "tests" / "data" / "sample_tickets.json"


def main() -> None:
    items = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    runnable = build_triage_runnable()
    correct = 0
    parse_failures = 0
    call_failures = 0
    for item in items:
        ticket = Ticket(**item)  # Ticket requires category; triage_ticket only uses the description
        try:
            result = triage_ticket(ticket, runnable=runnable)
        except (ClientError, BotoCoreError):
            # ReadTimeoutError / ConnectTimeoutError derive from BotoCoreError, not ClientError.
            call_failures += 1
            print(f"ID: {item['ticket_id']}, CALL FAILURE")
            continue
        except ValueError:  # bad JSON or failed TriageResult validation
            parse_failures += 1
            print(f"ID: {item['ticket_id']}, PARSE FAILURE")
            continue
        print(f"ID: {item['ticket_id']}, expected: {item['category']}, got: {result.category}")
        if result.category == item["category"]:
            correct += 1
    print(
        f"baseline: {correct}/{len(items)} category accuracy, "
        f"{parse_failures} parse failures, {call_failures} call failures"
    )


if __name__ == "__main__":
    main()
