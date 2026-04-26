'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { apiLogin, apiLogout, apiRefresh, apiMe, AuthUser } from '@/lib/authApi';

interface AuthState {
  user: AuthUser | null;
  accessToken: string | null;
  loading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    loading: true,
  });

  // On every mount/refresh: restore session via HttpOnly refresh token cookie (set by backend)
  useEffect(() => {
    (async () => {
      const token = await apiRefresh();
      if (token) {
        try {
          const user = await apiMe(token);
          setState({ user, accessToken: token, loading: false });
          return;
        } catch {
          // refresh token invalid or expired
        }
      }
      setState({ user: null, accessToken: null, loading: false });
    })();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const { access_token, user } = await apiLogin(email, password);
    // Access token lives in memory only — never written to any storage
    setState({ user, accessToken: access_token, loading: false });
  }, []);

  const logout = useCallback(async () => {
    await apiLogout();
    setState({ user: null, accessToken: null, loading: false });
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
