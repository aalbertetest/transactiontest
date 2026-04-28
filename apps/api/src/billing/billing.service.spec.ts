import { BillingService } from './billing.service';
import { MockStripeProvider } from './providers/mock-stripe.provider';
import { NotFoundException } from '@nestjs/common';

describe('BillingService', () => {
  let prisma: any;
  let svc: BillingService;
  const provider = new MockStripeProvider();

  beforeEach(() => {
    prisma = {
      plan: { findMany: jest.fn(), findUnique: jest.fn() },
      user: { findUnique: jest.fn() },
      subscription: {
        findFirst: jest.fn(),
        create: jest.fn().mockImplementation(({ data }) => ({ ...data })),
        update: jest.fn().mockImplementation(({ data, where }) => ({ ...where, ...data })),
      },
      invoice: {
        create: jest.fn().mockResolvedValue({}),
        findMany: jest.fn().mockResolvedValue([]),
      },
    };
    svc = new BillingService(prisma, provider);
  });

  it('throws when subscribing to a missing plan', async () => {
    prisma.plan.findUnique.mockResolvedValue(null);
    await expect(svc.subscribeDirectly('u1', 'plan_x')).rejects.toBeInstanceOf(NotFoundException);
  });

  it('creates a subscription and an invoice', async () => {
    prisma.plan.findUnique.mockResolvedValue({
      id: 'plan_pro',
      priceCents: 1900,
      currency: 'usd',
    });
    prisma.subscription.findFirst.mockResolvedValue(null);
    const sub = await svc.subscribeDirectly('u1', 'plan_pro');
    expect(sub.userId).toBe('u1');
    expect(sub.planId).toBe('plan_pro');
    expect(prisma.invoice.create).toHaveBeenCalled();
  });

  it('handles checkout.session.completed webhook', async () => {
    prisma.plan.findUnique.mockResolvedValue({ id: 'plan_pro', priceCents: 1900, currency: 'usd' });
    prisma.subscription.findFirst.mockResolvedValue(null);
    const res = await svc.handleWebhook({
      id: 'evt_1',
      type: 'checkout.session.completed',
      data: { userId: 'u1', planId: 'plan_pro' },
    });
    expect(res.handled).toBe(true);
    expect(prisma.subscription.create).toHaveBeenCalled();
  });
});

describe('MockStripeProvider', () => {
  const provider = new MockStripeProvider();

  it('verifies a correctly signed webhook', () => {
    const payload = JSON.stringify({ id: 'e', type: 'invoice.paid', data: {} });
    const { createHmac } = require('crypto');
    const sig = createHmac('sha256', 'secret').update(payload).digest('hex');
    expect(provider.verifyWebhook(payload, sig, 'secret').type).toBe('invoice.paid');
  });

  it('rejects bad signatures', () => {
    expect(() => provider.verifyWebhook('{}', 'bad', 'secret')).toThrow();
  });
});
