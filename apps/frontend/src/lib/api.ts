import type { AuthTokens, AuthUser, BillingInvoice, BillingPlan, BillingSubscription } from '@saas/shared';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:3000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `HTTP ${response.status}`);
  }

  return (await response.json()) as T;
}

export interface AuthResponse extends AuthTokens {
  user: AuthUser;
}

export const api = {
  register: (payload: { name: string; email: string; password: string }) =>
    request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  login: (payload: { email: string; password: string }) =>
    request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  oauthLogin: (payload: { provider: 'github' | 'google'; code: string }) =>
    request<AuthResponse>('/auth/oauth/callback', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  plans: () => request<BillingPlan[]>('/billing/plans'),

  createSubscription: (token: string, planCode: 'starter' | 'growth' | 'enterprise') =>
    request<BillingSubscription>('/billing/subscriptions', {
      method: 'POST',
      headers: {
        authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ planCode }),
    }),

  invoices: (token: string) =>
    request<BillingInvoice[]>('/billing/invoices', {
      headers: {
        authorization: `Bearer ${token}`,
      },
    }),
};
