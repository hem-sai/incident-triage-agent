import json
from pathlib import Path

from api.models import Ticket

DEFAULT_PATH = Path("tests/data/sample_tickets.json")


def load_tickets(path: Path = DEFAULT_PATH) -> list[Ticket]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Ticket.model_validate(item) for item in raw]


if __name__ == "__main__":
    print(f"Loaded {len(load_tickets())} tickets")
