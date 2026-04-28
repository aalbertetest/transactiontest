import { useEffect, useMemo, useState } from 'react';
import type { AuthUser, BillingInvoice, BillingPlan, BillingSubscription } from '@saas/shared';
import { Dashboard } from './components/Dashboard';
import { LoginForm } from './components/LoginForm';
import { api } from './lib/api';

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [plans, setPlans] = useState<BillingPlan[]>([]);
  const [invoices, setInvoices] = useState<BillingInvoice[]>([]);
  const [subscription, setSubscription] = useState<BillingSubscription | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.plans().then(setPlans).catch((loadError) => {
      setError(loadError instanceof Error ? loadError.message : 'Failed to load plans');
    });
  }, []);

  const authenticated = useMemo(() => Boolean(token && user), [token, user]);

  async function refreshInvoices(nextToken: string) {
    const fetched = await api.invoices(nextToken);
    setInvoices(fetched);
  }

  async function handleRegister(payload: { name: string; email: string; password: string }) {
    const response = await api.register(payload);
    setToken(response.accessToken);
    setUser(response.user);
    await refreshInvoices(response.accessToken);
  }

  async function handleLogin(payload: { email: string; password: string }) {
    const response = await api.login(payload);
    setToken(response.accessToken);
    setUser(response.user);
    await refreshInvoices(response.accessToken);
  }

  async function handleOAuth(provider: 'github' | 'google', code: string) {
    const response = await api.oauthLogin({ provider, code });
    setToken(response.accessToken);
    setUser(response.user);
    await refreshInvoices(response.accessToken);
  }

  async function handleSubscribe(planCode: 'starter' | 'growth' | 'enterprise') {
    if (!token) {
      return;
    }
    const result = await api.createSubscription(token, planCode);
    setSubscription(result);
    await refreshInvoices(token);
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-100">
      <div className="mx-auto max-w-5xl">
        <h1 className="mb-2 text-3xl font-bold">Production-ready SaaS Monorepo</h1>
        <p className="mb-8 text-sm text-slate-400">
          React + Tailwind frontend, NestJS backend, JWT/OAuth auth, mocked Stripe-like billing.
        </p>

        {!authenticated ? (
          <LoginForm onLogin={handleLogin} onRegister={handleRegister} onOAuth={handleOAuth} />
        ) : (
          <Dashboard
            userEmail={user?.email ?? 'unknown'}
            plans={plans}
            invoices={invoices}
            subscription={subscription}
            onSubscribe={handleSubscribe}
            onRefreshInvoices={() => (token ? refreshInvoices(token) : Promise.resolve())}
          />
        )}

        {error ? <p className="mt-4 text-rose-400">{error}</p> : null}
      </div>
    </main>
  );
}

export default App;
