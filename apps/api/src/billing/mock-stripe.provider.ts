import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import type { PlanId } from '@saas/shared';
import { randomUUID } from 'node:crypto';
import { BillingProvider } from './billing-provider';

@Injectable()
export class MockStripeBillingProvider implements BillingProvider {
  constructor(private readonly config: ConfigService) {}

  async createCheckoutSession(customerId: string, planId: PlanId) {
    const id = `cs_mock_${randomUUID()}`;
    return {
      id,
      customerId,
      planId,
      url: `https://billing.example.test/checkout/${id}`,
    };
  }

  async createPortalSession(customerId: string) {
    const id = `bps_mock_${randomUUID()}`;
    return {
      id,
      customerId,
      url: `https://billing.example.test/portal/${id}`,
    };
  }

  async verifyWebhook(payload: unknown, signature: string) {
    if (signature !== this.config.get('STRIPE_WEBHOOK_SECRET', 'whsec_mock')) {
      throw new UnauthorizedException('Invalid billing webhook signature');
    }
    return { type: 'customer.subscription.updated', data: payload };
  }
}
