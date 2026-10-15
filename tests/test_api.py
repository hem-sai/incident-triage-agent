import pytest
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient

from api.main import app, get_bedrock_client

VALID_TICKET = {
    "ticket_id": "T-001",
    "description": "VPN drops every 10 minutes",
    "category": "network",
    "severity": "high",
    "created_at": "2026-10-01T09:30:00",
}


class FakeClient:
    def __init__(self, text=None, error=None):
        self.text = text
        self.error = error

    def converse(self, **kwargs):
        if self.error:
            raise self.error
        return {
            "output": {"message": {"role": "assistant",
                                   "content": [{"text": self.text}]}},
            "usage": {"inputTokens": 10, "outputTokens": 5, "totalTokens": 15},
        }


def make_client(fake):
    app.dependency_overrides[get_bedrock_client] = lambda: fake
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()   # why? think before you copy this


def test_create_ticket_returns_triage():
    fake = FakeClient(text='{"category": "network", "severity": "high", "confidence": 0.9}')
    client = make_client(fake)

    response = client.post("/tickets", json=VALID_TICKET)

    assert response.status_code == 200
    assert response.json() == {
        "category": "network",
        "severity": "high",
        "confidence": 0.9,
    }


def test_empty_description_returns_422():
    client = make_client(FakeClient(text="unused"))
    response = client.post("/tickets", json={**VALID_TICKET, "description": ""})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "bad_text",
    [
        "this is not json",
        '{"category": "network", "severity": "high"}',
        '{"category": "network", "severity": "high", "confidence": 1.7}',
    ],
    ids=["non-json", "missing-key", "confidence-out-of-range"],
)
def test_bad_model_output_returns_502(bad_text):
    client = make_client(FakeClient(text=bad_text))
    response = client.post("/tickets", json=VALID_TICKET)
    assert response.status_code == 502


def test_aws_error_returns_503():
    error = ClientError({"Error": {"Code": "ThrottlingException", "Message": "x"}}, "Converse")
    client = make_client(FakeClient(error=error))
    response = client.post("/tickets", json=VALID_TICKET)
    assert response.status_code == 503
