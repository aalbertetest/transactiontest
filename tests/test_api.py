import httpx
import pytest

from mini_search.api import create_app


@pytest.mark.anyio
async def test_api_index_and_search(tmp_path) -> None:
    app = create_app(db_path=str(tmp_path / "api.db"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        index_resp = await client.post(
            "/documents",
            json={
                "documents": [
                    {
                        "url": "https://example.com/doc",
                        "title": "Example",
                        "content": "Search engines index content.",
                    }
                ]
            },
        )
        assert index_resp.status_code == 200
        assert index_resp.json()["indexed"] == 1

        search_resp = await client.post("/search", json={"query": "search", "top_k": 5})
        assert search_resp.status_code == 200
        results = search_resp.json()["results"]
        assert results
        assert results[0]["url"] == "https://example.com/doc"

        stats_resp = await client.get("/stats")
        assert stats_resp.status_code == 200
        assert stats_resp.json()["total_docs"] == 1
