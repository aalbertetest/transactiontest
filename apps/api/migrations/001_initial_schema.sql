create extension if not exists pgcrypto;

create table if not exists organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  email text not null unique,
  name text not null,
  password_hash text,
  oauth_provider text,
  oauth_subject text,
  created_at timestamptz not null default now()
);

create unique index if not exists users_oauth_identity_idx
  on users(oauth_provider, oauth_subject)
  where oauth_provider is not null and oauth_subject is not null;
