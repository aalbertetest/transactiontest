import uvicorn

from mini_search.coordinator import Shard, create_coordinator_app


def main() -> None:
    shards = [
        Shard(shard_id="shard1", base_url="http://localhost:8001"),
        Shard(shard_id="shard2", base_url="http://localhost:8002"),
    ]
    app = create_coordinator_app(shards)
    uvicorn.run(app, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
