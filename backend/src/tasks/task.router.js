import { Router } from 'express';
import {
  createTaskSchema,
  updateTaskSchema,
  listTasksQuery,
} from './task.schema.js';

export function taskRouter(svc, requireUser) {
  const r = Router();
  r.use(requireUser);

  r.get('/', async (req, res, next) => {
    try {
      const q = listTasksQuery.parse(req.query);
      res.json(await svc.list(req.userId, q));
    } catch (e) {
      next(e);
    }
  });

  r.get('/:id', async (req, res, next) => {
    try {
      res.json(await svc.get(req.userId, req.params.id));
    } catch (e) {
      next(e);
    }
  });

  r.post('/', async (req, res, next) => {
    try {
      const input = createTaskSchema.parse(req.body);
      res.status(201).json(await svc.create(req.userId, input));
    } catch (e) {
      next(e);
    }
  });

  r.patch('/:id', async (req, res, next) => {
    try {
      const patch = updateTaskSchema.parse(req.body);
      res.json(await svc.update(req.userId, req.params.id, patch));
    } catch (e) {
      next(e);
    }
  });

  r.delete('/:id', async (req, res, next) => {
    try {
      await svc.delete(req.userId, req.params.id);
      res.status(204).end();
    } catch (e) {
      next(e);
    }
  });

  return r;
}
