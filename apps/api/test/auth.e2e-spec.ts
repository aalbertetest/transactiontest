import { Test } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { execSync } from 'child_process';
import { mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

import { AppModule } from '../src/app.module';

/**
 * End-to-end integration tests against a real SQLite database.
 * The database is migrated and seeded once per test run.
 */
describe('Auth + Billing (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const dir = mkdtempSync(join(tmpdir(), 'saas-e2e-'));
    process.env.DATABASE_URL = `file:${join(dir, 'test.db')}`;
    process.env.JWT_ACCESS_SECRET = 'test-access';
    process.env.JWT_REFRESH_SECRET = 'test-refresh';
    process.env.JWT_ACCESS_TTL = '60';
    process.env.JWT_REFRESH_TTL = '600';

    execSync('npx prisma migrate deploy', {
      stdio: 'inherit',
      cwd: join(__dirname, '..'),
      env: process.env,
    });
    execSync('npx ts-node prisma/seed.ts', {
      stdio: 'inherit',
      cwd: join(__dirname, '..'),
      env: process.env,
    });

    const moduleRef = await Test.createTestingModule({ imports: [AppModule] }).compile();
    app = moduleRef.createNestApplication();
    app.setGlobalPrefix('api');
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
  }, 120_000);

  afterAll(async () => {
    await app?.close();
  });

  let access: string;
  let refresh: string;

  it('registers a user', async () => {
    const res = await request(app.getHttpServer())
      .post('/api/auth/register')
      .send({ email: 'e2e@example.com', password: 'password123', name: 'E2E' })
      .expect(201);
    expect(res.body.accessToken).toBeDefined();
    access = res.body.accessToken;
    refresh = res.body.refreshToken;
  });

  it('refreshes tokens', async () => {
    const res = await request(app.getHttpServer())
      .post('/api/auth/refresh')
      .send({ refreshToken: refresh })
      .expect(200);
    expect(res.body.accessToken).toBeDefined();
    refresh = res.body.refreshToken;
  });

  it('returns the current user', async () => {
    const res = await request(app.getHttpServer())
      .get('/api/users/me')
      .set('Authorization', `Bearer ${access}`)
      .expect(200);
    expect(res.body.email).toBe('e2e@example.com');
  });

  it('lists plans', async () => {
    const res = await request(app.getHttpServer()).get('/api/billing/plans').expect(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBeGreaterThan(0);
  });

  it('subscribes the user to a plan', async () => {
    const res = await request(app.getHttpServer())
      .post('/api/billing/subscribe')
      .set('Authorization', `Bearer ${access}`)
      .send({ planId: 'plan_pro' })
      .expect(201);
    expect(res.body.status).toBe('active');
  });
});
