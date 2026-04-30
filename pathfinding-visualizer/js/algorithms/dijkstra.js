/**
 * Dijkstra's Algorithm for pathfinding.
 *
 * A greedy algorithm that always expands the node with the smallest known
 * distance from the start. Handles weighted edges and guarantees the
 * shortest path on graphs with non-negative weights.
 *
 * On an unweighted grid it behaves identically to BFS, but it generalises
 * to weighted grids where each cell can have a movement cost > 1.
 *
 * Time:  O(V log V) with a binary heap; O(V²) with a naive scan.
 * Space: O(V) for the distance table, parent map, and priority queue.
 *
 * Pseudocode:
 *   function Dijkstra(start, end):
 *       dist[start] = 0
 *       pq ← MinHeap containing start
 *       while pq is not empty:
 *           node ← pq.extractMin()
 *           if node == end: return reconstructPath(parent, end)
 *           for neighbor in getNeighbors(node):
 *               alt = dist[node] + weight(node, neighbor)
 *               if alt < dist[neighbor]:
 *                   dist[neighbor] = alt
 *                   parent[neighbor] = node
 *                   pq.decreaseKey(neighbor, alt)
 *       return null
 */
export function dijkstra(grid, startNode, endNode) {
  const visitedInOrder = [];
  const allNodes = getAllNodes(grid);

  startNode.distance = 0;

  const unvisited = new MinHeap();
  for (const node of allNodes) {
    unvisited.insert(node);
  }

  while (unvisited.size() > 0) {
    const closest = unvisited.extractMin();

    if (closest.isWall) continue;
    if (closest.distance === Infinity) break;

    closest.isVisited = true;
    visitedInOrder.push(closest);

    if (closest === endNode) return visitedInOrder;

    updateUnvisitedNeighbors(closest, grid, unvisited);
  }

  return visitedInOrder;
}

function updateUnvisitedNeighbors(node, grid, heap) {
  const neighbors = getUnvisitedNeighbors(node, grid);
  for (const neighbor of neighbors) {
    const alt = node.distance + neighbor.weight;
    if (alt < neighbor.distance) {
      neighbor.distance = alt;
      neighbor.previousNode = node;
      heap.decreaseKey(neighbor);
    }
  }
}

function getUnvisitedNeighbors(node, grid) {
  const neighbors = [];
  const { row, col } = node;
  const rows = grid.length;
  const cols = grid[0].length;

  if (row > 0) neighbors.push(grid[row - 1][col]);
  if (row < rows - 1) neighbors.push(grid[row + 1][col]);
  if (col > 0) neighbors.push(grid[row][col - 1]);
  if (col < cols - 1) neighbors.push(grid[row][col + 1]);

  return neighbors.filter(n => !n.isVisited && !n.isWall);
}

function getAllNodes(grid) {
  const nodes = [];
  for (const row of grid) {
    for (const node of row) {
      nodes.push(node);
    }
  }
  return nodes;
}

/**
 * Binary min-heap keyed on node.distance.
 * Supports O(log n) insert, extractMin, and decreaseKey.
 */
class MinHeap {
  constructor() {
    this._heap = [];
    this._indices = new Map();
  }

  size() {
    return this._heap.length;
  }

  insert(node) {
    this._heap.push(node);
    const idx = this._heap.length - 1;
    this._indices.set(node, idx);
    this._bubbleUp(idx);
  }

  extractMin() {
    const min = this._heap[0];
    const last = this._heap.pop();
    this._indices.delete(min);
    if (this._heap.length > 0) {
      this._heap[0] = last;
      this._indices.set(last, 0);
      this._sinkDown(0);
    }
    return min;
  }

  decreaseKey(node) {
    const idx = this._indices.get(node);
    if (idx !== undefined) {
      this._bubbleUp(idx);
    }
  }

  _bubbleUp(idx) {
    while (idx > 0) {
      const parentIdx = (idx - 1) >> 1;
      if (this._heap[idx].distance >= this._heap[parentIdx].distance) break;
      this._swap(idx, parentIdx);
      idx = parentIdx;
    }
  }

  _sinkDown(idx) {
    const length = this._heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;

      if (left < length && this._heap[left].distance < this._heap[smallest].distance) {
        smallest = left;
      }
      if (right < length && this._heap[right].distance < this._heap[smallest].distance) {
        smallest = right;
      }
      if (smallest === idx) break;
      this._swap(idx, smallest);
      idx = smallest;
    }
  }

  _swap(i, j) {
    [this._heap[i], this._heap[j]] = [this._heap[j], this._heap[i]];
    this._indices.set(this._heap[i], i);
    this._indices.set(this._heap[j], j);
  }
}
