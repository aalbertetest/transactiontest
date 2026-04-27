"""Payment, ledger, fraud, and idempotency tests."""

import pytest
from fastapi.testclient import TestClient


def _register(client: TestClient, email: str, password: str = "password123") -> dict:
    r = client.post("/v1/users", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()


def _token(client: TestClient, email: str, password: str = "password123") -> str:
    r = client.post("/v1/users/token", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_payment_balances_ledger(client: TestClient):
    a = _register(client, "a@example.com")
    b = _register(client, "b@example.com")
    tok = _token(client, "a@example.com")
    r = client.post(
        "/v1/payments",
        json={"payee_user_id": b["id"], "amount_cents": 10000},
        headers={"Authorization": f"Bearer {tok}"},
    )
    assert r.status_code == 201
    body = r.json()
    deb = sum(x["amount_cents"] for x in body["ledger"] if x["side"] == "debit")
    cred = sum(x["amount_cents"] for x in body["ledger"] if x["side"] == "credit")
    assert deb == cred


def test_idempotency_replay(client: TestClient):
    a = _register(client, "p1@example.com")
    b = _register(client, "p2@example.com")
    tok = _token(client, "p1@example.com")
    headers = {"Authorization": f"Bearer {tok}", "Idempotency-Key": "k-1"}
    payload = {"payee_user_id": b["id"], "amount_cents": 5000}
    r1 = client.post("/v1/payments", json=payload, headers=headers)
    assert r1.status_code == 201
    r2 = client.post("/v1/payments", json=payload, headers=headers)
    assert r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]


def test_idempotency_conflict(client: TestClient):
    a = _register(client, "c1@example.com")
    b = _register(client, "c2@example.com")
    tok = _token(client, "c1@example.com")
    headers = {"Authorization": f"Bearer {tok}", "Idempotency-Key": "same-key"}
    r1 = client.post(
        "/v1/payments",
        json={"payee_user_id": b["id"], "amount_cents": 1000},
        headers=headers,
    )
    assert r1.status_code == 201
    r2 = client.post(
        "/v1/payments",
        json={"payee_user_id": b["id"], "amount_cents": 2000},
        headers=headers,
    )
    assert r2.status_code == 409


def test_fraud_self_payment(client: TestClient):
    a = _register(client, "self@example.com")
    tok = _token(client, "self@example.com")
    r = client.post(
        "/v1/payments",
        json={"payee_user_id": a["id"], "amount_cents": 100},
        headers={"Authorization": f"Bearer {tok}"},
    )
    assert r.status_code == 403


def test_get_payment_forbidden_other_user(client: TestClient):
    a = _register(client, "x@example.com")
    b = _register(client, "y@example.com")
    c = _register(client, "z@example.com")
    tok_a = _token(client, "x@example.com")
    r = client.post(
        "/v1/payments",
        json={"payee_user_id": b["id"], "amount_cents": 100},
        headers={"Authorization": f"Bearer {tok_a}"},
    )
    pid = r.json()["id"]
    tok_c = _token(client, "z@example.com")
    r2 = client.get(f"/v1/payments/{pid}", headers={"Authorization": f"Bearer {tok_c}"})
    assert r2.status_code == 403
