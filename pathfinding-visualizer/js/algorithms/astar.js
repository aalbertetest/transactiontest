/**
 * A* (A-Star) pathfinding algorithm.
 *
 * An informed search that combines Dijkstra's actual cost (g) with a
 * heuristic estimate of remaining cost (h) to guide expansion toward
 * the goal.  With an admissible heuristic (never overestimates),
 * A* guarantees the shortest path while typically visiting far fewer
 * nodes than Dijkstra.
 *
 * f(n) = g(n) + h(n)
 *   g(n) = actual distance from start to n
 *   h(n) = heuristic estimate from n to end (Manhattan distance here)
 *
 * Time:  O(V log V) — same worst-case as Dijkstra, but the heuristic
 *        usually prunes the search space dramatically.
 * Space: O(V)
 *
 * Pseudocode:
 *   function AStar(start, end):
 *       g[start] = 0
 *       f[start] = h(start, end)
 *       openSet ← MinHeap containing start (keyed on f)
 *       while openSet is not empty:
 *           node ← openSet.extractMin()
 *           if node == end: return reconstructPath(parent, end)
 *           for neighbor in getNeighbors(node):
 *               tentativeG = g[node] + weight(node, neighbor)
 *               if tentativeG < g[neighbor]:
 *                   g[neighbor] = tentativeG
 *                   f[neighbor] = tentativeG + h(neighbor, end)
 *                   parent[neighbor] = node
 *                   openSet.insertOrUpdate(neighbor)
 *       return null
 */
export function astar(grid, startNode, endNode) {
  const visitedInOrder = [];

  startNode.distance = 0;
  startNode.heuristic = manhattanDistance(startNode, endNode);
  startNode.totalDistance = startNode.heuristic;

  const openSet = new MinHeap();
  openSet.insert(startNode);

  while (openSet.size() > 0) {
    const current = openSet.extractMin();

    if (current.isWall) continue;
    if (current.distance === Infinity) break;

    current.isVisited = true;
    visitedInOrder.push(current);

    if (current === endNode) return visitedInOrder;

    const neighbors = getUnvisitedNeighbors(current, grid);
    for (const neighbor of neighbors) {
      const tentativeG = current.distance + neighbor.weight;
      if (tentativeG < neighbor.distance) {
        neighbor.distance = tentativeG;
        neighbor.heuristic = manhattanDistance(neighbor, endNode);
        neighbor.totalDistance = tentativeG + neighbor.heuristic;
        neighbor.previousNode = current;

        if (openSet.contains(neighbor)) {
          openSet.decreaseKey(neighbor);
        } else {
          openSet.insert(neighbor);
        }
      }
    }
  }

  return visitedInOrder;
}

function manhattanDistance(a, b) {
  return Math.abs(a.row - b.row) + Math.abs(a.col - b.col);
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

class MinHeap {
  constructor() {
    this._heap = [];
    this._indices = new Map();
  }

  size() {
    return this._heap.length;
  }

  contains(node) {
    return this._indices.has(node);
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
      if (this._heap[idx].totalDistance >= this._heap[parentIdx].totalDistance) break;
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

      if (left < length && this._heap[left].totalDistance < this._heap[smallest].totalDistance) {
        smallest = left;
      }
      if (right < length && this._heap[right].totalDistance < this._heap[smallest].totalDistance) {
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
