import { describe, it, expect, beforeEach } from 'vitest';
import { useAuth } from './auth';

describe('auth store', () => {
  beforeEach(() => useAuth.getState().logout());

  it('sets and clears auth state', () => {
    useAuth.getState().setAuth(
      { id: '1', email: 'a@b.co', name: null, role: 'USER', createdAt: new Date().toISOString() },
      'access',
      'refresh',
    );
    expect(useAuth.getState().user?.email).toBe('a@b.co');
    expect(useAuth.getState().accessToken).toBe('access');
    useAuth.getState().logout();
    expect(useAuth.getState().user).toBeNull();
    expect(useAuth.getState().accessToken).toBeNull();
  });
});
