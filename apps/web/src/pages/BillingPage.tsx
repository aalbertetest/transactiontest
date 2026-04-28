import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import type { Plan } from '@saas/shared';

export function BillingPage() {
  const qc = useQueryClient();
  const plans = useQuery({
    queryKey: ['plans'],
    queryFn: async () => (await api.get<Plan[]>('/billing/plans')).data,
  });
  const subscription = useQuery({
    queryKey: ['subscription'],
    queryFn: async () => (await api.get('/billing/subscription')).data,
  });
  const invoices = useQuery({
    queryKey: ['invoices'],
    queryFn: async () => (await api.get('/billing/invoices')).data,
  });

  const subscribe = useMutation({
    mutationFn: async (planId: string) =>
      (await api.post('/billing/subscribe', { planId })).data,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['subscription'] });
      qc.invalidateQueries({ queryKey: ['invoices'] });
    },
  });

  const cancel = useMutation({
    mutationFn: async () => (await api.post('/billing/cancel')).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['subscription'] }),
  });

  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">Billing</h1>
        <p className="text-sm text-slate-600">
          Choose a plan. Subscriptions are processed by the mock provider.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {plans.data?.map((p: any) => {
          const features: string[] =
            typeof p.features === 'string' ? JSON.parse(p.features) : p.features;
          return (
            <div key={p.id} className="card flex flex-col">
              <h3 className="text-lg font-semibold">{p.name}</h3>
              <p className="mt-1 text-3xl font-bold">
                ${(p.priceCents / 100).toFixed(2)}
                <span className="text-base font-normal text-slate-500">/{p.interval}</span>
              </p>
              <ul className="mt-3 flex-1 list-disc space-y-1 pl-5 text-sm text-slate-700">
                {features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <button
                className="btn-primary mt-4"
                onClick={() => subscribe.mutate(p.id)}
                disabled={subscribe.isPending}
              >
                {subscribe.isPending ? 'Subscribing…' : 'Subscribe'}
              </button>
            </div>
          );
        })}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold">Current subscription</h2>
        {subscription.data ? (
          <div className="mt-2 flex items-center justify-between">
            <div className="text-sm">
              <div>
                <span className="font-medium">
                  {subscription.data.plan?.name ?? subscription.data.planId}
                </span>{' '}
                — {subscription.data.status}
              </div>
              <div className="text-slate-500">
                Renews {new Date(subscription.data.currentPeriodEnd).toLocaleDateString()}
              </div>
            </div>
            <button
              className="btn-ghost border border-slate-200"
              onClick={() => cancel.mutate()}
              disabled={cancel.isPending || subscription.data.cancelAtPeriodEnd}
            >
              {subscription.data.cancelAtPeriodEnd ? 'Cancellation scheduled' : 'Cancel'}
            </button>
          </div>
        ) : (
          <p className="mt-2 text-sm text-slate-600">No subscription yet.</p>
        )}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold">Invoices</h2>
        <ul className="mt-2 divide-y divide-slate-200 text-sm">
          {(invoices.data ?? []).map((inv: any) => (
            <li key={inv.id} className="flex items-center justify-between py-2">
              <span>{new Date(inv.createdAt).toLocaleDateString()}</span>
              <span>${(inv.amountCents / 100).toFixed(2)}</span>
              <span className="text-slate-500">{inv.status}</span>
            </li>
          ))}
          {(invoices.data ?? []).length === 0 && (
            <li className="py-2 text-slate-500">No invoices yet.</li>
          )}
        </ul>
      </div>
    </section>
  );
}
