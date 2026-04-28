export type BillingPlanCode = 'starter' | 'growth' | 'enterprise';

export interface BillingPlan {
  code: BillingPlanCode;
  name: string;
  amountCents: number;
  currency: 'USD';
  interval: 'month';
}

export interface BillingSubscription {
  id: string;
  providerSubscriptionId: string;
  planCode: BillingPlanCode;
  status: 'active' | 'cancelled' | 'past_due';
  startedAt: string;
  endedAt: string | null;
}

export interface BillingInvoice {
  id: string;
  providerInvoiceId: string;
  amountCents: number;
  currency: 'USD';
  status: 'open' | 'paid' | 'void';
  issuedAt: string;
  paidAt: string | null;
}

export interface AuthTokens {
  accessToken: string;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string;
}
