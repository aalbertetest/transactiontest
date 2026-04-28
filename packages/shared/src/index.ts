export type Role = 'USER' | 'ADMIN';

export interface PublicUser {
  id: string;
  email: string;
  name: string | null;
  role: Role;
  createdAt: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
}

export type SubscriptionStatus =
  | 'incomplete'
  | 'active'
  | 'past_due'
  | 'canceled'
  | 'trialing';

export interface Plan {
  id: string;
  name: string;
  priceCents: number;
  currency: 'usd';
  interval: 'month' | 'year';
  features: string[];
}

export interface Subscription {
  id: string;
  userId: string;
  planId: string;
  status: SubscriptionStatus;
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
}

export interface Invoice {
  id: string;
  userId: string;
  subscriptionId: string;
  amountCents: number;
  currency: 'usd';
  status: 'paid' | 'open' | 'void';
  createdAt: string;
}

export const PLANS: Plan[] = [
  {
    id: 'plan_free',
    name: 'Free',
    priceCents: 0,
    currency: 'usd',
    interval: 'month',
    features: ['1 project', 'Community support'],
  },
  {
    id: 'plan_pro',
    name: 'Pro',
    priceCents: 1900,
    currency: 'usd',
    interval: 'month',
    features: ['Unlimited projects', 'Priority support', 'Advanced analytics'],
  },
  {
    id: 'plan_team',
    name: 'Team',
    priceCents: 4900,
    currency: 'usd',
    interval: 'month',
    features: ['Everything in Pro', 'Team seats', 'SSO'],
  },
];
