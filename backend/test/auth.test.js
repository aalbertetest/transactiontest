import { describe, it, expect, beforeEach } from 'vitest';
import request from 'supertest';
import { buildApp } from '../src/app.js';
import { openDb } from '../src/db.js';

const config = {
  jwtSecret: 'a'.repeat(64),
  port: 0,
  dbPath: ':memory:',
  bcryptCost: 4, // fast for tests
  accessTtl: '15m',
  refreshTtlMs: 1000 * 60 * 60,
};

function app() {
  const db = openDb(':memory:');
  return buildApp({ config, db });
}

describe('auth', () => {
  let ctx;
  beforeEach(() => {
    ctx = app();
  });

  it('registers and returns access + refresh tokens', async () => {
    const res = await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'correcthorsebattery' });
    expect(res.status).toBe(201);
    expect(res.body.accessToken).toBeTypeOf('string');
    expect(res.body.refreshToken).toBeTypeOf('string');
  });

  it('rejects short passwords with 400', async () => {
    const res = await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'short' });
    expect(res.status).toBe(400);
  });

  it('returns generic invalid_credentials on wrong password (no enumeration)', async () => {
    await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'correcthorsebattery' });

    const wrongPw = await request(ctx.app)
      .post('/auth/login')
      .send({ email: 'a@example.com', password: 'wrongpasswordlong' });

    const noUser = await request(ctx.app)
      .post('/auth/login')
      .send({ email: 'nobody@example.com', password: 'wrongpasswordlong' });

    expect(wrongPw.status).toBe(401);
    expect(noUser.status).toBe(401);
    expect(wrongPw.body.error).toBe('invalid_credentials');
    expect(noUser.body.error).toBe('invalid_credentials');
  });

  it('rotates refresh tokens; old one stops working', async () => {
    const reg = await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'correcthorsebattery' });
    const oldRefresh = reg.body.refreshToken;

    const r1 = await request(ctx.app)
      .post('/auth/refresh')
      .send({ refreshToken: oldRefresh });
    expect(r1.status).toBe(200);

    const r2 = await request(ctx.app)
      .post('/auth/refresh')
      .send({ refreshToken: oldRefresh });
    expect(r2.status).toBe(401);
  });

  it('rejects duplicate email with 409', async () => {
    await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'correcthorsebattery' });
    const res = await request(ctx.app)
      .post('/auth/register')
      .send({ email: 'a@example.com', password: 'correcthorsebattery' });
    expect(res.status).toBe(409);
  });
});
