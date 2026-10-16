import logging

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
        self.calls = []

    def converse(self, **kwargs):
        self.calls.append(kwargs)
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

def test_logs_request_id_and_latency(caplog):
    caplog.set_level(logging.INFO, logger="triage")
    fake = FakeClient(text='{"category": "network", "severity": "high", "confidence": 0.9}')
    client = make_client(fake)
    client.post("/tickets", json=VALID_TICKET)
    msgs = [r.getMessage() for r in caplog.records if r.name == "triage"]
    assert len(msgs) == 1
    assert "request_id=" in msgs[0] and "latency_ms=" in msgs[0]
    assert "status=200" in msgs[0]
    assert "input_tokens=10" in msgs[0] and "output_tokens=5" in msgs[0]

def test_logs_on_502(caplog):
    caplog.set_level(logging.INFO, logger="triage")
    client = make_client(FakeClient(text="not json"))
    response = client.post("/tickets", json=VALID_TICKET)
    assert response.status_code == 502
    msgs = [r.getMessage() for r in caplog.records if r.name == "triage"]
    assert any("request_id=" in m and "latency_ms=" in m and "status=502" in m for m in msgs)

def test_logs_on_503(caplog):
    caplog.set_level(logging.INFO, logger="triage")
    error = ClientError({"Error": {"Code": "ThrottlingException", "Message": "x"}}, "Converse")
    client = make_client(FakeClient(error=error))
    response = client.post("/tickets", json=VALID_TICKET)
    assert response.status_code == 503
    msgs = [r.getMessage() for r in caplog.records if r.name == "triage"]
    assert any("request_id=" in m and "latency_ms=" in m and "status=503" in m for m in msgs)


@pytest.mark.parametrize(
    "description",
    [
        "VPN हर 10 मिनट में डिस्कनेक्ट हो जाता है",
        "VPN ప్రతి 10 నిమిషాలకు డిస్కనెక్ట్ అవుతుంది",
        "VPNが10分ごとに切断されます",
    ],
    ids=["hindi", "telugu", "japanese"],
)
def test_non_english_description_returns_200_and_logs(caplog, description):
    caplog.set_level(logging.INFO, logger="triage")
    fake = FakeClient(text='{"category": "network", "severity": "high", "confidence": 0.9}')
    client = make_client(fake)

    response = client.post("/tickets", json={**VALID_TICKET, "description": description})

    assert response.status_code == 200
    # the text survived JSON in and reached the prompt intact
    assert description in fake.calls[0]["messages"][0]["content"][0]["text"]
    # logging did not crash and still wrote its one line
    msgs = [r.getMessage() for r in caplog.records if r.name == "triage"]
    assert len(msgs) == 1 and "status=200" in msgs[0]
    # the ticket text itself must not be logged
    assert description not in msgs[0]
