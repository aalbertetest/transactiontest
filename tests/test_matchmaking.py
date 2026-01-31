def _issue_token(client, player_id: str) -> str:
    response = client.post("/auth/issue", json={"player_id": player_id})
    assert response.status_code == 200
    return response.json()["token"]


def test_matchmaking_flow(client):
    token_one = _issue_token(client, "player-one")
    token_two = _issue_token(client, "player-two")

    headers_one = {"X-Player-Id": "player-one", "X-Player-Token": token_one}
    headers_two = {"X-Player-Id": "player-two", "X-Player-Token": token_two}

    join_one = client.post(
        "/matchmaking/join",
        json={"player_id": "player-one", "region": "na", "skill": 10},
        headers=headers_one,
    )
    assert join_one.status_code == 200
    ticket_one = join_one.json()
    assert ticket_one["status"] == "queued"

    join_two = client.post(
        "/matchmaking/join",
        json={"player_id": "player-two", "region": "na", "skill": 12},
        headers=headers_two,
    )
    assert join_two.status_code == 200
    ticket_two = join_two.json()
    assert ticket_two["status"] == "matched"
    assert ticket_two["session_id"]

    status_one = client.get(
        f"/matchmaking/status/{ticket_one['ticket_id']}", headers=headers_one
    )
    assert status_one.status_code == 200
    assert status_one.json()["status"] == "matched"


def test_cancel_ticket(client):
    token = _issue_token(client, "player-three")
    headers = {"X-Player-Id": "player-three", "X-Player-Token": token}

    join = client.post(
        "/matchmaking/join",
        json={"player_id": "player-three", "region": "na", "skill": 5},
        headers=headers,
    )
    assert join.status_code == 200
    ticket_id = join.json()["ticket_id"]

    cancel = client.post(f"/matchmaking/cancel/{ticket_id}", headers=headers)
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"
