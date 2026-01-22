# Architecture

This document describes the architecture and data model used by the cache
implementations. The design mirrors Redis-style behavior while remaining small
enough for educational use and unit testing.

## High-Level Components

```
+--------------------+     +---------------------+
|  Client API        | --> |  Cluster Router     |
+--------------------+     +---------------------+
                                   |
                                   v
                         +---------------------+
                         |  Node (Primary)     |
                         |  - Store            |
                         |  - TTL              |
                         |  - Eviction         |
                         |  - Pub/Sub          |
                         |  - Persistence      |
                         +---------------------+
                             |           |
                             v           v
                      +------------+  +------------+
                      | Replica A |  | Replica B |
                      +------------+  +------------+
```

## Data Structures

### Entry

Each key maps to an entry containing:

- `value`: JSON-serializable payload
- `expires_at`: unix timestamp (ms) or `None`
- `version`: monotonically increasing integer for conflict resolution

### Store

- A hash map from key to entry
- An LRU list to track recency (key -> node in doubly linked list)

## TTL (Time To Live)

TTL is checked on:

1. Reads (lazy deletion)
2. Writes (pre-insert cleanup)
3. A periodic sweeper that scans expired entries

Expired entries are deleted and removed from the LRU list.

## Eviction Strategy

The default eviction policy is LRU:

- On `get`, move key to the head
- On `set`, insert at head
- When capacity is exceeded, evict from tail

The eviction policy is pluggable by implementing a simple interface.

## Sharding

Consistent hashing maps keys to primary nodes:

- Each node is represented by multiple virtual nodes on a hash ring
- The owner of a key is the first node clockwise from the key hash
- Replicas are chosen by walking clockwise to the next nodes

## Replication

Primary nodes replicate writes to their replicas:

- `set`, `delete`, and `expire` operations are serialized into replication
  messages.
- Replicas apply the same write with the primary's version.
- A simple in-process transport is provided; a real deployment would replace
  this with TCP/HTTP streams.

## Persistence

Two layers are supported:

1. **Snapshot**: periodic full dump of the store to a JSON file.
2. **Append-Only Log (AOF)**: line-delimited operations appended on every write.

Startup flow:

1. Load snapshot (if present)
2. Replay the append-only log

## Pub/Sub

Pub/Sub channels provide fan-out messaging:

- `subscribe(channel, handler)` registers a handler
- `publish(channel, payload)` delivers to local subscribers
- For clustered setups, publishes are optionally forwarded to replicas

Messages are not persisted.

## Clustering

The cluster router owns:

- Node membership
- Hash ring
- Replication factor

Reads route to the primary node. Writes route to the primary node, which
replicates to its configured replicas.

## Failure Model (Simplified)

This implementation assumes:

- Primary nodes are available
- No cross-primary conflict resolution
- Replicas are eventually consistent

These choices keep the design small while still illustrating core mechanisms.
