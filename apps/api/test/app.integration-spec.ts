import { INestApplication, ValidationPipe } from '@nestjs/common';
import { Test } from '@nestjs/testing';
import request from 'supertest';
import { AppModule } from '../src/app.module';

describe('API integration', () => {
  let app: INestApplication;

  beforeAll(async () => {
    process.env.JWT_SECRET = 'integration-secret';
    const moduleRef = await Test.createTestingModule({ imports: [AppModule] }).compile();
    app = moduleRef.createNestApplication();
    app.setGlobalPrefix('api');
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('reports health', async () => {
    await request(app.getHttpServer()).get('/api/health').expect(200).expect({ status: 'ok', service: 'api' });
  });

  it('logs in and reads the authenticated profile', async () => {
    const login = await request(app.getHttpServer())
      .post('/api/auth/login')
      .send({ email: 'founder@example.com', password: 'password' })
      .expect(201);

    await request(app.getHttpServer())
      .get('/api/auth/me')
      .set('Authorization', `Bearer ${login.body.accessToken}`)
      .expect(200)
      .expect(({ body }) => expect(body.user.email).toBe('founder@example.com'));
  });

  it('creates a mocked checkout session', async () => {
    await request(app.getHttpServer())
      .post('/api/billing/checkout')
      .send({ customerId: 'cus_demo', planId: 'growth' })
      .expect(201)
      .expect(({ body }) => expect(body.url).toContain('billing.example.test/checkout'));
  });
});
