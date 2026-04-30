/**
 * Grid model — owns the 2-D array of node objects and exposes helpers
 * for resetting, toggling walls, and relocating start/end markers.
 */

export function createNode(row, col) {
  return {
    row,
    col,
    isStart: false,
    isEnd: false,
    isWall: false,
    isVisited: false,
    previousNode: null,
    distance: Infinity,
    heuristic: 0,
    totalDistance: Infinity,
    weight: 1,
  };
}

export function createGrid(rows, cols) {
  const grid = [];
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < cols; c++) {
      row.push(createNode(r, c));
    }
    grid.push(row);
  }
  return grid;
}

export function resetGrid(grid) {
  for (const row of grid) {
    for (const node of row) {
      node.isVisited = false;
      node.previousNode = null;
      node.distance = Infinity;
      node.heuristic = 0;
      node.totalDistance = Infinity;
    }
  }
}

export function clearWalls(grid) {
  for (const row of grid) {
    for (const node of row) {
      node.isWall = false;
      node.weight = 1;
    }
  }
}

export function getShortestPath(endNode) {
  const path = [];
  let current = endNode;
  while (current !== null) {
    path.unshift(current);
    current = current.previousNode;
  }
  return path;
}
