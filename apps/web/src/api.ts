import type { Plan } from '@saas/shared';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

export interface SessionResponse {
  accessToken: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export async function fetchPlans(): Promise<Plan[]> {
  const response = await fetch(`${API_BASE_URL}/billing/plans`);
  if (!response.ok) {
    throw new Error('Unable to load plans');
  }
  return response.json();
}

export async function login(email: string, password: string): Promise<SessionResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error('Invalid email or password');
  }
  return response.json();
}
