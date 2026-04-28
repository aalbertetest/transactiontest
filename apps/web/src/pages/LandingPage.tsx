import { Link } from 'react-router-dom';

export function LandingPage() {
  return (
    <section className="grid gap-12 md:grid-cols-2 md:items-center">
      <div>
        <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
          A SaaS starter that ships with everything.
        </h1>
        <p className="mt-4 text-lg text-slate-600">
          Auth (JWT + OAuth), billing, migrations, tests, and CI — already wired up so you can
          focus on your product.
        </p>
        <div className="mt-8 flex gap-3">
          <Link to="/register" className="btn-primary">
            Create an account
          </Link>
          <Link to="/login" className="btn-ghost">
            I already have one
          </Link>
        </div>
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold">What's inside</h2>
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-700">
          <li>NestJS API with Prisma + SQLite/Postgres</li>
          <li>JWT access + refresh tokens, Google OAuth</li>
          <li>Mock Stripe-style billing & webhooks</li>
          <li>Vitest, Jest, supertest end-to-end</li>
          <li>GitHub Actions CI/CD pipeline</li>
        </ul>
      </div>
    </section>
  );
}
