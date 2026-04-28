import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/auth';

export function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-lg font-semibold tracking-tight">
            <span className="text-brand-600">SaaS</span>Starter
          </Link>
          <nav className="flex items-center gap-4 text-sm">
            {user ? (
              <>
                <NavLink to="/dashboard" className="text-slate-600 hover:text-slate-900">
                  Dashboard
                </NavLink>
                <NavLink to="/billing" className="text-slate-600 hover:text-slate-900">
                  Billing
                </NavLink>
                <span className="text-slate-500">{user.email}</span>
                <button
                  className="btn-ghost"
                  onClick={() => {
                    logout();
                    navigate('/');
                  }}
                >
                  Sign out
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" className="text-slate-600 hover:text-slate-900">
                  Sign in
                </NavLink>
                <NavLink to="/register" className="btn-primary">
                  Get started
                </NavLink>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-10">
        <Outlet />
      </main>
      <footer className="border-t border-slate-200 bg-white py-6 text-center text-sm text-slate-500">
        Built with NestJS, React, Tailwind, and Prisma.
      </footer>
    </div>
  );
}
