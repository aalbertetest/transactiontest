import type { PlanId } from '@saas/shared';

export interface CheckoutSession {
  id: string;
  url: string;
  customerId: string;
  planId: PlanId;
}

export interface BillingPortalSession {
  id: string;
  url: string;
  customerId: string;
}

export interface BillingProvider {
  createCheckoutSession(customerId: string, planId: PlanId): Promise<CheckoutSession>;
  createPortalSession(customerId: string): Promise<BillingPortalSession>;
  verifyWebhook(payload: unknown, signature: string): Promise<{ type: string; data: unknown }>;
}
