import { BillingService } from './billing.service';

describe('BillingService', () => {
  const prisma = {
    subscription: {
      create: jest.fn().mockResolvedValue({
        id: 'sub_local',
        providerSubscriptionId: 'sub_provider',
        planCode: 'starter',
        status: 'active',
        startedAt: new Date('2024-01-01T00:00:00.000Z'),
        endedAt: null,
      }),
    },
    invoice: {
      create: jest.fn().mockResolvedValue({}),
      findMany: jest.fn().mockResolvedValue([]),
      updateMany: jest.fn().mockResolvedValue({ count: 1 }),
    },
    billingEvent: {
      create: jest.fn().mockResolvedValue({ id: 'evt_1' }),
    },
  };

  const service = new BillingService(prisma as never);

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('creates subscription for known plan', async () => {
    const result = await service.createSubscription('user_1', 'starter');
    expect(result.planCode).toBe('starter');
    expect(result.status).toBe('active');
  });

  it('signs payload for webhook tests', () => {
    const signature = service.buildWebhookSignature('{"type":"invoice.paid"}');
    expect(signature).toHaveLength(64);
  });
});
