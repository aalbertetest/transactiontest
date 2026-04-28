/**
 * Provider abstraction so we can swap MockStripe for the real Stripe SDK
 * without touching call sites. The shape mirrors a subset of Stripe's API.
 */
export abstract class PaymentProvider {
  abstract createCustomer(params: { email: string; name?: string | null }): Promise<{ id: string }>;
  abstract createCheckoutSession(params: {
    customerId: string;
    planId: string;
    priceCents: number;
    successUrl: string;
    cancelUrl: string;
  }): Promise<{ id: string; url: string }>;
  abstract createSubscription(params: {
    customerId: string;
    planId: string;
  }): Promise<{ id: string; status: 'active'; currentPeriodEnd: Date }>;
  abstract cancelSubscription(id: string): Promise<{ id: string; cancelAtPeriodEnd: true }>;
  abstract verifyWebhook(payload: string, signature: string, secret: string): WebhookEvent;
}

export interface WebhookEvent {
  id: string;
  type:
    | 'checkout.session.completed'
    | 'invoice.paid'
    | 'customer.subscription.updated'
    | 'customer.subscription.deleted';
  data: any;
}
