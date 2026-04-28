import { formatCurrency, type Plan } from '@saas/shared';
import { useEffect, useState } from 'react';
import { fetchPlans, login, type SessionResponse } from './api';

const fallbackPlans: Plan[] = [
  {
    id: 'starter',
    name: 'Starter',
    monthlyPriceCents: 1900,
    seatsIncluded: 3,
    features: ['JWT auth', 'Mock billing portal', 'Email support'],
  },
];

export function App() {
  const [plans, setPlans] = useState<Plan[]>(fallbackPlans);
  const [session, setSession] = useState<SessionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlans().then(setPlans).catch(() => setPlans(fallbackPlans));
  }, []);

  async function handleDemoLogin() {
    setError(null);
    try {
      setSession(await login('founder@example.com', 'password'));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Login failed');
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <section className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-16">
        <div className="rounded-3xl bg-slate-950 px-8 py-12 text-white shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-cyan-300">Production SaaS</p>
          <h1 className="mt-4 max-w-3xl text-5xl font-bold tracking-tight">Launch-ready monorepo with auth, billing, migrations, and CI/CD.</h1>
          <p className="mt-6 max-w-2xl text-lg text-slate-300">React, NestJS, shared TypeScript contracts, mocked Stripe-style billing, and testable service boundaries.</p>
          <button onClick={handleDemoLogin} className="mt-8 rounded-full bg-cyan-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-200">Try demo login</button>
          {session && <p className="mt-4 text-cyan-100">Signed in as {session.user.email}</p>}
          {error && <p className="mt-4 text-red-200">{error}</p>}
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {plans.map((plan) => (
            <article key={plan.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold">{plan.name}</h2>
              <p className="mt-2 text-4xl font-black">{formatCurrency(plan.monthlyPriceCents)}<span className="text-base font-medium text-slate-500">/mo</span></p>
              <p className="mt-3 text-slate-600">Includes {plan.seatsIncluded} seats.</p>
              <ul className="mt-5 space-y-2 text-sm text-slate-700">
                {plan.features.map((feature) => <li key={feature}>- {feature}</li>)}
              </ul>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
