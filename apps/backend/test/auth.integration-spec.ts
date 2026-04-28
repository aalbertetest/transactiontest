import { INestApplication } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import { AppModule } from '../src/app.module';
import { BillingService } from '../src/billing/billing.service';

describe('Auth + Billing Integration', () => {
  let app: INestApplication;
  let moduleRef: TestingModule;

  beforeAll(async () => {
    moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('registers, logs in, subscribes, and processes mock webhook', async () => {
    const email = `test-${Date.now()}@example.com`;
    const password = 'Password123!';

    await request(app.getHttpServer()).post('/auth/register').send({
      name: 'Integration User',
      email,
      password,
    }).expect(201);

    const loginResponse = await request(app.getHttpServer()).post('/auth/login').send({
      email,
      password,
    }).expect(201);

    const token = loginResponse.body.accessToken as string;
    expect(token).toBeDefined();

    const subscriptionResponse = await request(app.getHttpServer())
      .post('/billing/subscriptions')
      .set('authorization', `Bearer ${token}`)
      .send({ planCode: 'starter' })
      .expect(201);

    expect(subscriptionResponse.body.status).toBe('active');

    const invoicesResponse = await request(app.getHttpServer())
      .get('/billing/invoices')
      .set('authorization', `Bearer ${token}`)
      .expect(200);

    const [firstInvoice] = invoicesResponse.body as Array<{ id: string }>;
    expect(firstInvoice?.id).toBeDefined();

    const billingService = moduleRef.get(BillingService);
    const payload = {
      type: 'invoice.paid',
      data: {
        invoiceId: firstInvoice.id,
      },
    };
    const rawPayload = JSON.stringify(payload);
    const signature = billingService.buildWebhookSignature(rawPayload);

    await request(app.getHttpServer())
      .post('/billing/webhooks/mock')
      .set('x-mock-signature', signature)
      .send(payload)
      .expect(201);

    const paidInvoicesResponse = await request(app.getHttpServer())
      .get('/billing/invoices')
      .set('authorization', `Bearer ${token}`)
      .expect(200);

    expect(paidInvoicesResponse.body[0].status).toBe('paid');
  });

  it('supports mocked oauth callback flow', async () => {
    const oauthResponse = await request(app.getHttpServer())
      .post('/auth/oauth/callback')
      .send({
        provider: 'github',
        code: 'oauthabc',
      })
      .expect(201);

    expect(oauthResponse.body.accessToken).toBeDefined();
    expect(oauthResponse.body.user.email).toContain('@github.oauth.local');
  });
});
