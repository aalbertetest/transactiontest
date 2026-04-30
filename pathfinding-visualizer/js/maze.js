/**
 * Maze generation algorithms for creating interesting test patterns.
 */

export function generateRandomMaze(grid, density = 0.3) {
  for (const row of grid) {
    for (const node of row) {
      if (node.isStart || node.isEnd) continue;
      node.isWall = Math.random() < density;
    }
  }
}

export function generateRecursiveDivisionMaze(grid) {
  for (const row of grid) {
    for (const node of row) {
      if (!node.isStart && !node.isEnd) node.isWall = false;
    }
  }

  const rows = grid.length;
  const cols = grid[0].length;
  const walls = [];

  divide(grid, 0, rows - 1, 0, cols - 1, chooseOrientation(cols, rows), walls);
  return walls;
}

function divide(grid, rowStart, rowEnd, colStart, colEnd, orientation, walls) {
  if (rowEnd - rowStart < 2 || colEnd - colStart < 2) return;

  const horizontal = orientation === 'HORIZONTAL';

  const wallRow = horizontal
    ? randomEven(rowStart + 1, rowEnd - 1)
    : rowStart;
  const wallCol = horizontal
    ? colStart
    : randomEven(colStart + 1, colEnd - 1);

  const passageRow = horizontal
    ? wallRow
    : randomOdd(rowStart, rowEnd);
  const passageCol = horizontal
    ? randomOdd(colStart, colEnd)
    : wallCol;

  const dRow = horizontal ? 0 : 1;
  const dCol = horizontal ? 1 : 0;

  const length = horizontal ? colEnd - colStart + 1 : rowEnd - rowStart + 1;

  let r = wallRow;
  let c = wallCol;

  for (let i = 0; i < length; i++) {
    if (r !== passageRow || c !== passageCol) {
      const node = grid[r]?.[c];
      if (node && !node.isStart && !node.isEnd) {
        node.isWall = true;
        walls.push(node);
      }
    }
    r += dRow;
    c += dCol;
  }

  if (horizontal) {
    divide(grid, rowStart, wallRow - 1, colStart, colEnd, chooseOrientation(colEnd - colStart + 1, wallRow - rowStart), walls);
    divide(grid, wallRow + 1, rowEnd, colStart, colEnd, chooseOrientation(colEnd - colStart + 1, rowEnd - wallRow), walls);
  } else {
    divide(grid, rowStart, rowEnd, colStart, wallCol - 1, chooseOrientation(wallCol - colStart, rowEnd - rowStart + 1), walls);
    divide(grid, rowStart, rowEnd, wallCol + 1, colEnd, chooseOrientation(colEnd - wallCol, rowEnd - rowStart + 1), walls);
  }
}

function chooseOrientation(width, height) {
  if (width < height) return 'HORIZONTAL';
  if (height < width) return 'VERTICAL';
  return Math.random() < 0.5 ? 'HORIZONTAL' : 'VERTICAL';
}

function randomEven(min, max) {
  const val = Math.floor(Math.random() * ((max - min) / 2 + 1)) * 2 + min;
  return val % 2 === 0 ? val : val - 1;
}

function randomOdd(min, max) {
  const val = Math.floor(Math.random() * ((max - min) / 2 + 1)) * 2 + min + 1;
  return val % 2 !== 0 ? val : val - 1;
}
