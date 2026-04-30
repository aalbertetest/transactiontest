/**
 * Depth-First Search (DFS) pathfinding algorithm.
 *
 * Explores as far as possible along each branch before backtracking.
 * Does NOT guarantee the shortest path — it returns the first path found,
 * which may be long and winding.
 *
 * Time:  O(V + E) — each vertex and edge visited at most once.
 * Space: O(V)     — the explicit stack and visited set.
 *
 * Pseudocode:
 *   function DFS(start, end):
 *       stack ← [start]
 *       visited ← {start}
 *       parent ← {}
 *       while stack is not empty:
 *           node ← stack.pop()
 *           if node == end: return reconstructPath(parent, end)
 *           for neighbor in getNeighbors(node):
 *               if neighbor not in visited and neighbor is not a wall:
 *                   visited.add(neighbor)
 *                   parent[neighbor] = node
 *                   stack.push(neighbor)
 *       return null   // no path
 */
export function dfs(grid, startNode, endNode) {
  const visitedInOrder = [];
  const stack = [startNode];
  startNode.isVisited = true;

  while (stack.length > 0) {
    const current = stack.pop();
    visitedInOrder.push(current);

    if (current === endNode) {
      return visitedInOrder;
    }

    const neighbors = getUnvisitedNeighbors(current, grid);
    for (const neighbor of neighbors) {
      neighbor.isVisited = true;
      neighbor.previousNode = current;
      stack.push(neighbor);
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
