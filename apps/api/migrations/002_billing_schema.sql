create table if not exists subscriptions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references organizations(id),
  provider text not null,
  provider_customer_id text not null,
  provider_subscription_id text,
  plan_id text not null check (plan_id in ('starter', 'growth', 'scale')),
  status text not null default 'incomplete',
  current_period_end timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists subscriptions_provider_customer_idx
  on subscriptions(provider, provider_customer_id);
