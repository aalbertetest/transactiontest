import { Router } from 'express';
import { credentialsSchema, refreshSchema } from './auth.schema.js';
import { AuthError } from './auth.service.js';
import { rateLimit } from '../middleware/rateLimit.js';

export function authRouter(svc) {
  const r = Router();

  r.post(
    '/register',
    rateLimit({ key: (req) => req.ip ?? 'anon', max: 20, windowMs: 60_000 }),
    async (req, res, next) => {
      try {
        const creds = credentialsSchema.parse(req.body);
        const tokens = await svc.register(creds);
        res.status(201).json(tokens);
      } catch (e) {
        next(e);
      }
    },
  );

  r.post(
    '/login',
    rateLimit({
      key: (req) => `${req.ip ?? 'anon'}:${(req.body?.email ?? '').toLowerCase()}`,
      max: 10,
      windowMs: 60_000,
    }),
    async (req, res, next) => {
      try {
        const creds = credentialsSchema.parse(req.body);
        const tokens = await svc.login(creds);
        res.json(tokens);
      } catch (e) {
        next(e);
      }
    },
  );

  r.post('/refresh', async (req, res, next) => {
    try {
      const { refreshToken } = refreshSchema.parse(req.body ?? {});
      res.json(await svc.refresh(refreshToken));
    } catch (e) {
      next(e);
    }
  });

  r.post('/logout', async (req, res, next) => {
    try {
      const { refreshToken } = refreshSchema.parse(req.body ?? {});
      await svc.logout(refreshToken);
      res.status(204).end();
    } catch (e) {
      next(e);
    }
  });

  return r;
}

export { AuthError };
