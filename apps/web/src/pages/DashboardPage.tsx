import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useAuth } from '../store/auth';

export function DashboardPage() {
  const { user } = useAuth();
  const { data: subscription } = useQuery({
    queryKey: ['subscription'],
    queryFn: async () => (await api.get('/billing/subscription')).data,
  });

  return (
    <section className="grid gap-6 md:grid-cols-2">
      <div className="card">
        <h2 className="text-lg font-semibold">Welcome{user?.name ? `, ${user.name}` : ''}</h2>
        <p className="mt-1 text-sm text-slate-600">{user?.email}</p>
        <p className="mt-4 text-sm text-slate-700">
          This is your dashboard. Wire it up to your domain models next.
        </p>
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold">Plan</h2>
        {subscription ? (
          <p className="mt-2 text-sm">
            <span className="font-medium">{subscription.plan?.name ?? subscription.planId}</span>{' '}
            <span className="text-slate-500">— {subscription.status}</span>
          </p>
        ) : (
          <p className="mt-2 text-sm text-slate-600">No active subscription. Visit Billing.</p>
        )}
      </div>
    </section>
  );
}
