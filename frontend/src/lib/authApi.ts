/**
 * Auth API — handles all auth-related HTTP calls.
 * Access token is returned and stored in memory (never localStorage).
 * Refresh token is an HttpOnly cookie managed by the browser.
 */

import axios from 'axios';

const AUTH_BASE = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api'}/auth`;

const authClient = axios.create({
  baseURL: AUTH_BASE,
  withCredentials: true, // needed so the HttpOnly refresh-token cookie is sent
  timeout: 10000,
});

export interface AuthUser {
  id: number;
  email: string;
  name: string;
  email_verified: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  user: AuthUser;
}

function extractError(err: unknown): string {
  if (axios.isAxiosError(err)) {
    return err.response?.data?.error || err.message;
  }
  return 'Something went wrong.';
}

export async function apiSignup(name: string, email: string, password: string): Promise<string> {
  try {
    const res = await authClient.post('/signup', { name, email, password });
    return res.data.message;
  } catch (err) {
    throw new Error(extractError(err));
  }
}

export async function apiLogin(email: string, password: string): Promise<LoginResponse> {
  try {
    const res = await authClient.post<LoginResponse>('/login', { email, password });
    return res.data;
  } catch (err) {
    throw new Error(extractError(err));
  }
}

export async function apiLogout(): Promise<void> {
  try {
    await authClient.post('/logout');
  } catch {
    // best effort
  }
}

export async function apiRefresh(): Promise<string | null> {
  try {
    const res = await authClient.post<{ access_token: string }>('/refresh');
    return res.data.access_token;
  } catch {
    return null;
  }
}

export async function apiMe(accessToken: string): Promise<AuthUser> {
  const res = await authClient.get<{ user: AuthUser }>('/me', {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return res.data.user;
}
