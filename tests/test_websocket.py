def _issue_token(client, player_id: str) -> str:
    response = client.post("/auth/issue", json={"player_id": player_id})
    assert response.status_code == 200
    return response.json()["token"]


def test_websocket_state_sync(client):
    token_one = _issue_token(client, "player-one")
    token_two = _issue_token(client, "player-two")

    headers_one = {"X-Player-Id": "player-one", "X-Player-Token": token_one}
    headers_two = {"X-Player-Id": "player-two", "X-Player-Token": token_two}

    join_one = client.post(
        "/matchmaking/join",
        json={"player_id": "player-one", "region": "na", "skill": 10},
        headers=headers_one,
    )
    join_two = client.post(
        "/matchmaking/join",
        json={"player_id": "player-two", "region": "na", "skill": 12},
        headers=headers_two,
    )

    session_id = join_two.json()["session_id"]
    assert session_id

    with client.websocket_connect(
        f"/ws/game/{session_id}?player_id=player-one&token={token_one}"
    ) as ws_one:
        initial_one = ws_one.receive_json()

        with client.websocket_connect(
            f"/ws/game/{session_id}?player_id=player-two&token={token_two}"
        ) as ws_two:
            initial_two = ws_two.receive_json()

            ws_one.send_json({"type": "input", "seq": 1, "dx": 1, "dy": 0, "dt": 0.05})

            update_one = ws_one.receive_json()
            update_two = ws_two.receive_json()

            assert update_one["type"] == "state"
            assert update_two["type"] == "state"
            assert (
                update_one["players"]["player-one"]["x"]
                > initial_one["players"]["player-one"]["x"]
            )
            assert (
                update_two["players"]["player-one"]["x"]
                == update_one["players"]["player-one"]["x"]
            )
            assert "player-two" in initial_two["players"]
