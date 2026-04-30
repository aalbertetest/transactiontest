import { Visualizer } from './visualizer.js';

document.addEventListener('DOMContentLoaded', () => {
  const gridEl = document.getElementById('grid');
  const statsEl = document.getElementById('stats');
  const viz = new Visualizer(gridEl, statsEl);

  document.getElementById('btn-bfs').addEventListener('click', () => viz.run('bfs'));
  document.getElementById('btn-dfs').addEventListener('click', () => viz.run('dfs'));
  document.getElementById('btn-dijkstra').addEventListener('click', () => viz.run('dijkstra'));
  document.getElementById('btn-astar').addEventListener('click', () => viz.run('astar'));

  document.getElementById('btn-clear-path').addEventListener('click', () => viz.clearVisualization());
  document.getElementById('btn-clear-board').addEventListener('click', () => viz.clearBoard());

  document.getElementById('btn-maze-random').addEventListener('click', () => viz.generateMaze('random'));
  document.getElementById('btn-maze-recursive').addEventListener('click', () => viz.generateMaze('recursive'));

  document.getElementById('speed-select').addEventListener('change', e => {
    viz.speed = e.target.value;
  });

  document.getElementById('grid-size').addEventListener('change', e => {
    const [rows, cols] = e.target.value.split('x').map(Number);
    viz.resize(rows, cols);
  });

  const infoToggle = document.getElementById('info-toggle');
  const infoPanel = document.getElementById('info-panel');
  infoToggle.addEventListener('click', () => {
    infoPanel.classList.toggle('collapsed');
    infoToggle.textContent = infoPanel.classList.contains('collapsed')
      ? 'Show Algorithm Details'
      : 'Hide Algorithm Details';
  });
});
