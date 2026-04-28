import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../store/auth';

export function ProtectedRoute() {
  const { accessToken } = useAuth();
  const location = useLocation();
  if (!accessToken) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return <Outlet />;
}
