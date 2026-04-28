import { Injectable, BadRequestException } from '@nestjs/common';
import { createHmac, randomUUID } from 'crypto';
import { PaymentProvider, WebhookEvent } from '../payment-provider';

/**
 * MockStripeProvider: an in-process implementation that mimics a Stripe-like
 * billing flow with deterministic, signed webhooks. Useful for development,
 * tests, and demos without external network calls or accounts.
 */
@Injectable()
export class MockStripeProvider extends PaymentProvider {
  async createCustomer(params: { email: string; name?: string | null }) {
    return { id: `cus_${randomUUID().slice(0, 12)}` };
  }

  async createCheckoutSession(params: {
    customerId: string;
    planId: string;
    priceCents: number;
    successUrl: string;
    cancelUrl: string;
  }) {
    const id = `cs_${randomUUID().slice(0, 16)}`;
    return { id, url: `${params.successUrl}?session_id=${id}&plan=${params.planId}` };
  }

  async createSubscription(params: { customerId: string; planId: string }) {
    return {
      id: `sub_${randomUUID().slice(0, 12)}`,
      status: 'active' as const,
      currentPeriodEnd: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    };
  }

  async cancelSubscription(id: string) {
    return { id, cancelAtPeriodEnd: true as const };
  }

  verifyWebhook(payload: string, signature: string, secret: string): WebhookEvent {
    const expected = createHmac('sha256', secret).update(payload).digest('hex');
    if (expected !== signature) throw new BadRequestException('Invalid webhook signature');
    try {
      return JSON.parse(payload) as WebhookEvent;
    } catch {
      throw new BadRequestException('Invalid webhook payload');
    }
  }
}
