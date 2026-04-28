import type { BillingInvoice, BillingPlan, BillingSubscription } from '@saas/shared';

interface DashboardProps {
  plans: BillingPlan[];
  invoices: BillingInvoice[];
  subscription: BillingSubscription | null;
  onSubscribe: (planCode: 'starter' | 'growth' | 'enterprise') => Promise<void>;
  onRefreshInvoices: () => Promise<void>;
  userEmail: string;
}

export function Dashboard({
  plans,
  invoices,
  subscription,
  onSubscribe,
  onRefreshInvoices,
  userEmail,
}: DashboardProps) {
  return (
    <section className="mx-auto mt-8 max-w-3xl rounded-xl border border-slate-800 bg-slate-900 p-6">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">Billing dashboard</h2>
          <p className="text-sm text-slate-400">Signed in as {userEmail}</p>
        </div>
        <button className="rounded bg-slate-700 px-3 py-2 text-sm" onClick={onRefreshInvoices}>
          Refresh invoices
        </button>
      </header>

      <div className="grid gap-3 md:grid-cols-3">
        {plans.map((plan) => (
          <article key={plan.code} className="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <h3 className="font-semibold">{plan.name}</h3>
            <p className="text-sm text-slate-400">${(plan.amountCents / 100).toFixed(2)} / month</p>
            <button
              className="mt-3 w-full rounded bg-indigo-600 px-3 py-2 text-sm"
              onClick={() => onSubscribe(plan.code)}
            >
              Subscribe
            </button>
          </article>
        ))}
      </div>

      <div className="mt-6">
        <h3 className="font-semibold">Active subscription</h3>
        {subscription ? (
          <p className="text-sm text-emerald-400">
            {subscription.planCode} ({subscription.status})
          </p>
        ) : (
          <p className="text-sm text-slate-400">No active subscription yet.</p>
        )}
      </div>

      <div className="mt-6">
        <h3 className="font-semibold">Invoices</h3>
        {invoices.length === 0 ? (
          <p className="text-sm text-slate-400">No invoices generated yet.</p>
        ) : (
          <ul className="mt-2 space-y-2 text-sm">
            {invoices.map((invoice) => (
              <li key={invoice.id} className="rounded border border-slate-800 bg-slate-950 px-3 py-2">
                <span className="font-medium">{invoice.providerInvoiceId}</span> - ${' '}
                {(invoice.amountCents / 100).toFixed(2)} - {invoice.status}
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
