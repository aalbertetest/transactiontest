import { ZodError } from 'zod';
import { AuthError } from '../auth/auth.service.js';
import { NotFoundError, ForbiddenError } from '../tasks/task.service.js';

export function errorHandler(err, req, res, _next) {
  if (err instanceof ZodError) {
    return res.status(400).json({ error: 'invalid_request', issues: err.issues });
  }
  if (err instanceof AuthError) {
    if (err.code === 'email_taken') {
      return res.status(409).json({ error: 'email_taken' });
    }
    if (err.code === 'invalid_token') {
      return res.status(401).json({ error: 'invalid_token' });
    }
    return res.status(401).json({ error: 'invalid_credentials' });
  }
  if (err instanceof NotFoundError) {
    return res.status(404).json({ error: 'not_found' });
  }
  if (err instanceof ForbiddenError) {
    return res.status(403).json({ error: 'forbidden' });
  }
  console.error('[error]', err);
  res.status(500).json({ error: 'internal' });
}
