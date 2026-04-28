import axios, { AxiosError, AxiosInstance } from 'axios';
import { useAuth } from '../store/auth';

const baseURL = import.meta.env.VITE_API_URL ?? '/api';

export const api: AxiosInstance = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = useAuth.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let refreshing: Promise<string | null> | null = null;

api.interceptors.response.use(
  (r) => r,
  async (error: AxiosError) => {
    const original: any = error.config;
    if (error.response?.status === 401 && !original?._retry) {
      original._retry = true;
      refreshing ??= refreshTokens();
      const newAccess = await refreshing;
      refreshing = null;
      if (newAccess) {
        original.headers = { ...original.headers, Authorization: `Bearer ${newAccess}` };
        return api(original);
      }
    }
    return Promise.reject(error);
  },
);

async function refreshTokens(): Promise<string | null> {
  const { refreshToken, setTokens, logout } = useAuth.getState();
  if (!refreshToken) return null;
  try {
    const res = await axios.post(`${baseURL}/auth/refresh`, { refreshToken });
    setTokens(res.data.accessToken, res.data.refreshToken);
    return res.data.accessToken as string;
  } catch {
    logout();
    return null;
  }
}
