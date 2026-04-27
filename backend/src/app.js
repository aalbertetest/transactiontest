import express from 'express';
import { openDb } from './db.js';
import { EventBus } from './events/bus.js';

import { UserRepo } from './auth/user.repo.js';
import { RefreshTokenRepo } from './auth/refresh.repo.js';
import { AuthService } from './auth/auth.service.js';
import { authRouter } from './auth/auth.router.js';

import { TaskRepo } from './tasks/task.repo.js';
import { TaskService } from './tasks/task.service.js';
import { taskRouter } from './tasks/task.router.js';

import { NotificationRepo } from './notifications/notification.repo.js';
import { UserPrefsRepo } from './notifications/prefs.repo.js';
import { registerNotificationDispatcher } from './notifications/dispatcher.js';
import { NotificationWorker } from './notifications/worker.js';
import { ConsoleTransport } from './notifications/transports.js';

import { makeRequireUser } from './middleware/requireUser.js';
import { errorHandler } from './middleware/error.js';

export function buildApp({ config, db: providedDb, transports } = {}) {
  if (!config) throw new Error('config_required');
  const db = providedDb ?? openDb(config.dbPath);
  const bus = new EventBus();

  const users = new UserRepo(db);
  const refreshTokens = new RefreshTokenRepo(db);
  const tasks = new TaskRepo(db);
  const notes = new NotificationRepo(db);
  const prefs = new UserPrefsRepo(db);

  const auth = new AuthService({ users, refreshTokens, config, bus });
  const taskSvc = new TaskService({ repo: tasks, bus });

  registerNotificationDispatcher({ bus, notes, prefs, users });

  const worker = new NotificationWorker({
    repo: notes,
    transports: transports ?? { console: new ConsoleTransport() },
  });

  const app = express();
  app.use(express.json({ limit: '256kb' }));
  app.get('/health', (_req, res) => res.json({ ok: true }));
  app.use('/auth', authRouter(auth));
  app.use('/tasks', taskRouter(taskSvc, makeRequireUser(auth)));
  app.use(errorHandler);

  return { app, db, bus, worker, services: { auth, tasks: taskSvc }, repos: { users, tasks, notes, prefs, refreshTokens } };
}
