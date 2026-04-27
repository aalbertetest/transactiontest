import { loadConfig } from './config.js';
import { buildApp } from './app.js';

const config = loadConfig();
const { app, worker } = buildApp({ config });

worker.start({ intervalMs: 1000 });

const server = app.listen(config.port, () => {
  console.log(`[tasks-backend] listening on http://localhost:${config.port}`);
});

function shutdown(signal) {
  console.log(`[tasks-backend] received ${signal}, shutting down`);
  worker.stop();
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 5000).unref();
}
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
