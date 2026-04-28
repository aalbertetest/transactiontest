import type { BillingPlan } from '@saas/shared';

export const BILLING_PLANS: BillingPlan[] = [
  {
    code: 'starter',
    name: 'Starter',
    amountCents: 1500,
    currency: 'USD',
    interval: 'month',
  },
  {
    code: 'growth',
    name: 'Growth',
    amountCents: 4900,
    currency: 'USD',
    interval: 'month',
  },
  {
    code: 'enterprise',
    name: 'Enterprise',
    amountCents: 19900,
    currency: 'USD',
    interval: 'month',
  },
];
