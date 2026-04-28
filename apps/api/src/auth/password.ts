import { createHash, pbkdf2Sync, timingSafeEqual } from 'node:crypto';

export function hashPassword(password: string, salt = 'demo-salt'): string {
  const digest = pbkdf2Sync(password, salt, 120_000, 32, 'sha256').toString('hex');
  return `pbkdf2_sha256$120000$${salt}$${digest}`;
}

export function verifyPassword(password: string, storedHash: string): boolean {
  const [algorithm, iterations, salt, digest] = storedHash.split('$');
  if (algorithm !== 'pbkdf2_sha256' || !iterations || !salt || !digest) {
    return false;
  }

  const candidate = pbkdf2Sync(password, salt, Number(iterations), 32, 'sha256');
  const expected = Buffer.from(digest, 'hex');
  return candidate.length === expected.length && timingSafeEqual(candidate, expected);
}

export const oauthSubjectForDemo = (token: string) =>
  createHash('sha256').update(token).digest('hex') ===
  createHash('sha256').update('valid-google-demo-code').digest('hex')
    ? 'google-oauth-demo-subject'
    : token;
