from __future__ import annotations


def register_user(client, username: str) -> str:
    response = client.post(
        "/auth/register",
        json={"username": username, "password": "supersecure"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def create_channel(client, token: str, name: str) -> str:
    response = client.post(
        "/channels",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name},
    )
    assert response.status_code == 200
    return response.json()["id"]


def join_channel(client, token: str, channel_id: str) -> None:
    response = client.post(
        f"/channels/{channel_id}/join",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def recv_until(ws, expected_type: str, max_events: int = 6):
    for _ in range(max_events):
        payload = ws.receive_json()
        if payload.get("type") == expected_type:
            return payload
    raise AssertionError(f"Did not receive {expected_type}")


def test_websocket_message_delivery(client):
    token_a = register_user(client, "alice")
    token_b = register_user(client, "bob")
    channel_id = create_channel(client, token_a, "general")
    join_channel(client, token_b, channel_id)

    with client.websocket_connect(f"/ws?token={token_a}") as ws_a:
        with client.websocket_connect(f"/ws?token={token_b}") as ws_b:
            ws_a.send_json(
                {
                    "type": "message",
                    "channel_id": channel_id,
                    "content": "hello world",
                }
            )

            ack = recv_until(ws_a, "ack")
            assert ack["message_id"]

            delivered = recv_until(ws_b, "message")
            assert delivered["message"]["content"] == "hello world"
            assert delivered["message"]["channel_id"] == channel_id
