import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../lib/api';
import { useAuth } from '../store/auth';

export function OAuthCallback() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { setTokens, setUser } = useAuth();

  useEffect(() => {
    const access = params.get('access');
    const refresh = params.get('refresh');
    if (!access || !refresh) {
      navigate('/login');
      return;
    }
    setTokens(access, refresh);
    api.get('/users/me').then(({ data }) => {
      setUser(data);
      navigate('/dashboard');
    });
  }, [params, navigate, setTokens, setUser]);

  return <p className="text-center text-sm text-slate-600">Completing sign in…</p>;
}
