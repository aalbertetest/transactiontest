from __future__ import annotations


def test_register_and_login(client):
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "supersecure"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    me = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "alice"

    login = client.post(
        "/auth/login",
        json={"username": "alice", "password": "supersecure"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]
