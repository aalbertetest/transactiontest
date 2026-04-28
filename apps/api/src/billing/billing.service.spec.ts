import { BadRequestException } from '@nestjs/common';
import { Test } from '@nestjs/testing';
import { BILLING_PROVIDER, BillingService } from './billing.service';

describe('BillingService', () => {
  it('creates checkout sessions through the provider', async () => {
    const provider = { createCheckoutSession: jest.fn().mockResolvedValue({ id: 'cs_1' }) };
    const module = await Test.createTestingModule({
      providers: [BillingService, { provide: BILLING_PROVIDER, useValue: provider }],
    }).compile();

    await expect(module.get(BillingService).createCheckoutSession('cus_1', 'growth')).resolves.toEqual({ id: 'cs_1' });
  });

  it('rejects unknown plans', async () => {
    const module = await Test.createTestingModule({
      providers: [BillingService, { provide: BILLING_PROVIDER, useValue: {} }],
    }).compile();

    await expect(module.get(BillingService).createCheckoutSession('cus_1', 'unknown')).rejects.toBeInstanceOf(BadRequestException);
  });
});
