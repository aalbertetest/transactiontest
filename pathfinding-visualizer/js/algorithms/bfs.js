/**
 * Breadth-First Search (BFS) pathfinding algorithm.
 *
 * Explores all neighbors at the current depth before moving deeper.
 * Guarantees the shortest path on unweighted grids because it visits
 * nodes in order of increasing distance from the start.
 *
 * Time:  O(V + E) — every vertex and edge visited at most once.
 * Space: O(V)     — the queue and visited set can hold all vertices.
 *
 * Pseudocode:
 *   function BFS(start, end):
 *       queue ← [start]
 *       visited ← {start}
 *       parent ← {}
 *       while queue is not empty:
 *           node ← queue.dequeue()
 *           if node == end: return reconstructPath(parent, end)
 *           for neighbor in getNeighbors(node):
 *               if neighbor not in visited and neighbor is not a wall:
 *                   visited.add(neighbor)
 *                   parent[neighbor] = node
 *                   queue.enqueue(neighbor)
 *       return null   // no path
 */
export function bfs(grid, startNode, endNode) {
  const visitedInOrder = [];
  const queue = [startNode];
  startNode.isVisited = true;

  while (queue.length > 0) {
    const current = queue.shift();
    visitedInOrder.push(current);

    if (current === endNode) {
      return visitedInOrder;
    }

    const neighbors = getUnvisitedNeighbors(current, grid);
    for (const neighbor of neighbors) {
      neighbor.isVisited = true;
      neighbor.previousNode = current;
      queue.push(neighbor);
    }
  }

  return visitedInOrder;
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
