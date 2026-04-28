import { BadRequestException, Inject, Injectable } from '@nestjs/common';
import { isPlanId, plans, type PlanId } from '@saas/shared';
import type { BillingProvider } from './billing-provider';

export const BILLING_PROVIDER = Symbol('BILLING_PROVIDER');

@Injectable()
export class BillingService {
  constructor(@Inject(BILLING_PROVIDER) private readonly provider: BillingProvider) {}

  getPlans() {
    return plans;
  }

  async createCheckoutSession(customerId: string, planId: string) {
    if (!isPlanId(planId)) {
      throw new BadRequestException('Unknown plan');
    }
    return this.provider.createCheckoutSession(customerId, planId as PlanId);
  }

  createPortalSession(customerId: string) {
    return this.provider.createPortalSession(customerId);
  }

  handleWebhook(payload: unknown, signature: string) {
    return this.provider.verifyWebhook(payload, signature);
  }
}
