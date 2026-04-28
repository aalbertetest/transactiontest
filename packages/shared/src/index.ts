export type PlanId = 'starter' | 'growth' | 'scale';

export interface Plan {
  id: PlanId;
  name: string;
  monthlyPriceCents: number;
  seatsIncluded: number;
  features: string[];
}

export const plans: Plan[] = [
  {
    id: 'starter',
    name: 'Starter',
    monthlyPriceCents: 1900,
    seatsIncluded: 3,
    features: ['JWT auth', 'Mock billing portal', 'Email support'],
  },
  {
    id: 'growth',
    name: 'Growth',
    monthlyPriceCents: 4900,
    seatsIncluded: 10,
    features: ['OAuth login', 'Team management', 'Priority support'],
  },
  {
    id: 'scale',
    name: 'Scale',
    monthlyPriceCents: 14900,
    seatsIncluded: 50,
    features: ['SSO-ready architecture', 'Audit logs', 'Dedicated success'],
  },
];

export const formatCurrency = (cents: number, currency = 'USD') =>
  new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(cents / 100);

export const isPlanId = (value: string): value is PlanId =>
  plans.some((plan) => plan.id === value);
