/**
 * Visualizer — handles DOM rendering, animation, and user interaction.
 *
 * Performance notes for large grids:
 *  - Cells are rendered once; only CSS classes are toggled during animation.
 *  - Animation uses requestAnimationFrame batches instead of per-cell setTimeout.
 *  - The grid uses CSS Grid layout with fixed cell sizes for GPU-friendly rendering.
 *  - For grids larger than ~100×100, consider canvas-based rendering (see scaling notes).
 */

import { createGrid, resetGrid, clearWalls, getShortestPath } from './grid.js';
import { bfs } from './algorithms/bfs.js';
import { dfs } from './algorithms/dfs.js';
import { dijkstra } from './algorithms/dijkstra.js';
import { astar } from './algorithms/astar.js';
import { generateRandomMaze, generateRecursiveDivisionMaze } from './maze.js';

const ANIMATION_SPEED = { fast: 5, medium: 20, slow: 50 };

export class Visualizer {
  constructor(containerEl, statsEl) {
    this.container = containerEl;
    this.statsEl = statsEl;
    this.rows = 25;
    this.cols = 50;
    this.grid = [];
    this.startPos = { row: 12, col: 5 };
    this.endPos = { row: 12, col: 44 };
    this.isRunning = false;
    this.animationFrames = [];
    this.speed = 'medium';
    this.mouseDown = false;
    this.dragMode = null; // 'start' | 'end' | 'wall'
    this.cellElements = [];

    this._initGrid();
    this._render();
    this._bindEvents();
  }

  /* ─── Grid helpers ──────────────────────────────────────────── */

  _initGrid() {
    this.grid = createGrid(this.rows, this.cols);
    this.grid[this.startPos.row][this.startPos.col].isStart = true;
    this.grid[this.endPos.row][this.endPos.col].isEnd = true;
  }

  resize(rows, cols) {
    this.cancelAnimation();
    this.rows = rows;
    this.cols = cols;
    this.startPos = { row: Math.floor(rows / 2), col: Math.floor(cols * 0.1) };
    this.endPos = { row: Math.floor(rows / 2), col: Math.floor(cols * 0.9) };
    this._initGrid();
    this._render();
  }

  /* ─── DOM rendering ─────────────────────────────────────────── */

  _render() {
    this.container.innerHTML = '';
    this.container.style.gridTemplateColumns = `repeat(${this.cols}, 1fr)`;
    this.cellElements = [];

    const fragment = document.createDocumentFragment();

    for (let r = 0; r < this.rows; r++) {
      const rowEls = [];
      for (let c = 0; c < this.cols; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.row = r;
        cell.dataset.col = c;

        if (this.grid[r][c].isStart) cell.classList.add('cell-start');
        if (this.grid[r][c].isEnd) cell.classList.add('cell-end');

        fragment.appendChild(cell);
        rowEls.push(cell);
      }
      this.cellElements.push(rowEls);
    }

    this.container.appendChild(fragment);
  }

  _getCellEl(row, col) {
    return this.cellElements[row]?.[col];
  }

  _refreshCellClass(node) {
    const el = this._getCellEl(node.row, node.col);
    if (!el) return;

    el.className = 'cell';
    if (node.isStart) el.classList.add('cell-start');
    else if (node.isEnd) el.classList.add('cell-end');
    else if (node.isWall) el.classList.add('cell-wall');
  }

  /* ─── User interaction ──────────────────────────────────────── */

  _bindEvents() {
    this.container.addEventListener('mousedown', e => this._onMouseDown(e));
    this.container.addEventListener('mouseover', e => this._onMouseMove(e));
    document.addEventListener('mouseup', () => this._onMouseUp());

    this.container.addEventListener('touchstart', e => this._onTouchStart(e), { passive: false });
    this.container.addEventListener('touchmove', e => this._onTouchMove(e), { passive: false });
    document.addEventListener('touchend', () => this._onMouseUp());
  }

  _cellFromEvent(e) {
    const target = e.target.closest('.cell');
    if (!target) return null;
    const row = +target.dataset.row;
    const col = +target.dataset.col;
    return this.grid[row][col];
  }

  _onMouseDown(e) {
    if (this.isRunning) return;
    e.preventDefault();
    this.mouseDown = true;
    const node = this._cellFromEvent(e);
    if (!node) return;

    if (node.isStart) this.dragMode = 'start';
    else if (node.isEnd) this.dragMode = 'end';
    else {
      this.dragMode = 'wall';
      node.isWall = !node.isWall;
      this._refreshCellClass(node);
    }
  }

  _onMouseMove(e) {
    if (!this.mouseDown || this.isRunning) return;
    const node = this._cellFromEvent(e);
    if (!node) return;

    if (this.dragMode === 'wall' && !node.isStart && !node.isEnd) {
      node.isWall = true;
      this._refreshCellClass(node);
    } else if (this.dragMode === 'start' && !node.isEnd && !node.isWall) {
      this.grid[this.startPos.row][this.startPos.col].isStart = false;
      this._refreshCellClass(this.grid[this.startPos.row][this.startPos.col]);
      node.isStart = true;
      this.startPos = { row: node.row, col: node.col };
      this._refreshCellClass(node);
    } else if (this.dragMode === 'end' && !node.isStart && !node.isWall) {
      this.grid[this.endPos.row][this.endPos.col].isEnd = false;
      this._refreshCellClass(this.grid[this.endPos.row][this.endPos.col]);
      node.isEnd = true;
      this.endPos = { row: node.row, col: node.col };
      this._refreshCellClass(node);
    }
  }

  _onMouseUp() {
    this.mouseDown = false;
    this.dragMode = null;
  }

  _onTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const target = document.elementFromPoint(touch.clientX, touch.clientY);
    if (target) this._onMouseDown({ target, preventDefault() {} });
  }

  _onTouchMove(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const target = document.elementFromPoint(touch.clientX, touch.clientY);
    if (target) this._onMouseMove({ target });
  }

  /* ─── Algorithm execution ───────────────────────────────────── */

  run(algorithmName) {
    if (this.isRunning) return;
    this.clearVisualization();
    resetGrid(this.grid);

    const startNode = this.grid[this.startPos.row][this.startPos.col];
    const endNode = this.grid[this.endPos.row][this.endPos.col];

    const t0 = performance.now();

    let visitedInOrder;
    switch (algorithmName) {
      case 'bfs':      visitedInOrder = bfs(this.grid, startNode, endNode);      break;
      case 'dfs':      visitedInOrder = dfs(this.grid, startNode, endNode);      break;
      case 'dijkstra': visitedInOrder = dijkstra(this.grid, startNode, endNode); break;
      case 'astar':    visitedInOrder = astar(this.grid, startNode, endNode);    break;
      default: return;
    }

    const t1 = performance.now();
    const shortestPath = getShortestPath(endNode);
    const pathFound = shortestPath.length > 1 || startNode === endNode;

    this._updateStats({
      algorithm: algorithmName.toUpperCase(),
      visited: visitedInOrder.length,
      pathLength: pathFound ? shortestPath.length : 0,
      time: (t1 - t0).toFixed(2),
    });

    this._animate(visitedInOrder, shortestPath);
  }

  /* ─── Animation engine (batched RAF for performance) ────────── */

  _animate(visitedInOrder, shortestPath) {
    this.isRunning = true;
    const delay = ANIMATION_SPEED[this.speed];
    const batchSize = Math.max(1, Math.ceil(visitedInOrder.length / 300));
    let i = 0;

    const animateVisited = () => {
      if (i >= visitedInOrder.length) {
        this._animatePath(shortestPath);
        return;
      }

      for (let b = 0; b < batchSize && i < visitedInOrder.length; b++, i++) {
        const node = visitedInOrder[i];
        if (!node.isStart && !node.isEnd) {
          const el = this._getCellEl(node.row, node.col);
          if (el) el.classList.add('cell-visited');
        }
      }

      this.animationFrames.push(setTimeout(animateVisited, delay));
    };

    animateVisited();
  }

  _animatePath(path) {
    const delay = ANIMATION_SPEED[this.speed] * 2;

    for (let i = 0; i < path.length; i++) {
      const timer = setTimeout(() => {
        const node = path[i];
        if (!node.isStart && !node.isEnd) {
          const el = this._getCellEl(node.row, node.col);
          if (el) {
            el.classList.remove('cell-visited');
            el.classList.add('cell-path');
          }
        }
        if (i === path.length - 1) {
          this.isRunning = false;
        }
      }, delay * i);

      this.animationFrames.push(timer);
    }

    if (path.length === 0) this.isRunning = false;
  }

  /* ─── Cleanup ───────────────────────────────────────────────── */

  cancelAnimation() {
    for (const id of this.animationFrames) clearTimeout(id);
    this.animationFrames = [];
    this.isRunning = false;
  }

  clearVisualization() {
    this.cancelAnimation();
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const el = this._getCellEl(r, c);
        if (el) {
          el.classList.remove('cell-visited', 'cell-path');
        }
      }
    }
  }

  clearBoard() {
    this.cancelAnimation();
    clearWalls(this.grid);
    resetGrid(this.grid);
    this._render();
  }

  /* ─── Maze ──────────────────────────────────────────────────── */

  generateMaze(type) {
    if (this.isRunning) return;
    this.clearBoard();

    if (type === 'random') {
      generateRandomMaze(this.grid, 0.3);
      this._render();
    } else if (type === 'recursive') {
      const walls = generateRecursiveDivisionMaze(this.grid);
      this._animateMaze(walls);
    }
  }

  _animateMaze(walls) {
    this.isRunning = true;
    const delay = Math.max(2, Math.floor(500 / walls.length));

    for (let i = 0; i < walls.length; i++) {
      const timer = setTimeout(() => {
        const node = walls[i];
        const el = this._getCellEl(node.row, node.col);
        if (el) el.classList.add('cell-wall');
        if (i === walls.length - 1) this.isRunning = false;
      }, delay * i);
      this.animationFrames.push(timer);
    }
  }

  /* ─── Stats panel ───────────────────────────────────────────── */

  _updateStats({ algorithm, visited, pathLength, time }) {
    if (!this.statsEl) return;
    this.statsEl.innerHTML = `
      <div class="stat"><span class="stat-label">Algorithm</span><span class="stat-value">${algorithm}</span></div>
      <div class="stat"><span class="stat-label">Nodes Visited</span><span class="stat-value">${visited}</span></div>
      <div class="stat"><span class="stat-label">Path Length</span><span class="stat-value">${pathLength || 'No path'}</span></div>
      <div class="stat"><span class="stat-label">Compute Time</span><span class="stat-value">${time} ms</span></div>
    `;
  }
}
