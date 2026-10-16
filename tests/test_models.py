import pytest
from pydantic import ValidationError

from api.loader import load_tickets
from api.models import Ticket


@pytest.fixture
def valid_ticket_data() -> dict:
    return {
        "ticket_id": "T-001",
        "description": "VPN drops every 10 minutes",
        "category": "network",
        "severity": "high",
        "created_at": "2026-10-01T09:30:00",
    }


@pytest.mark.parametrize(
    "field, bad_value",
    [("severity", "urgent"), ("category", "printer"), ("description", "   "), ("ticket_id", "001")],
)
def test_ticket_rejects_bad_input(valid_ticket_data, field, bad_value):
    valid_ticket_data[field] = bad_value
    with pytest.raises(ValidationError):
        Ticket(**valid_ticket_data)


def test_all_sample_tickets_load():
    assert len(load_tickets()) == 20