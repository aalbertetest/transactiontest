import { useState } from 'react';

export interface LoginFormProps {
  onLogin: (payload: { email: string; password: string }) => Promise<void>;
  onRegister: (payload: { name: string; email: string; password: string }) => Promise<void>;
  onOAuth: (provider: 'github' | 'google', code: string) => Promise<void>;
}

export function LoginForm({ onLogin, onRegister, onOAuth }: LoginFormProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setError(null);

    try {
      if (mode === 'register') {
        await onRegister({ name, email, password });
      } else {
        await onLogin({ email, password });
      }
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to authenticate');
    }
  };

  return (
    <div className="mx-auto w-full max-w-md rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-lg">
      <h1 className="mb-3 text-2xl font-semibold">SaaS Auth</h1>
      <p className="mb-4 text-sm text-slate-400">JWT + mocked OAuth sign-in</p>

      <div className="mb-3 flex gap-2">
        <button
          className={`rounded px-3 py-1 text-sm ${mode === 'login' ? 'bg-indigo-500' : 'bg-slate-800'}`}
          onClick={() => setMode('login')}
          type="button"
        >
          Login
        </button>
        <button
          className={`rounded px-3 py-1 text-sm ${mode === 'register' ? 'bg-indigo-500' : 'bg-slate-800'}`}
          onClick={() => setMode('register')}
          type="button"
        >
          Register
        </button>
      </div>

      {mode === 'register' && (
        <input
          className="mb-3 w-full rounded bg-slate-800 px-3 py-2"
          placeholder="Name"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
      )}

      <input
        className="mb-3 w-full rounded bg-slate-800 px-3 py-2"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />

      <input
        className="mb-3 w-full rounded bg-slate-800 px-3 py-2"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />

      <button className="mb-3 w-full rounded bg-indigo-600 px-3 py-2 font-semibold" type="button" onClick={submit}>
        {mode === 'register' ? 'Create account' : 'Sign in'}
      </button>

      <button
        className="mb-3 w-full rounded bg-slate-700 px-3 py-2"
        type="button"
        onClick={() => onOAuth('github', 'frontend-demo-code')}
      >
        Continue with GitHub (mock)
      </button>

      <button
        className="w-full rounded bg-slate-700 px-3 py-2"
        type="button"
        onClick={() => onOAuth('google', 'frontend-demo-code')}
      >
        Continue with Google (mock)
      </button>

      {error ? <p className="mt-3 text-sm text-rose-400">{error}</p> : null}
    </div>
  );
}
