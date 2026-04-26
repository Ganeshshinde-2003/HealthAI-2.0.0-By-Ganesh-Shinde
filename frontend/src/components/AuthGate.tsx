'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { FullPageLoader } from '@/components/FullPageLoader';

// Wrap protected pages — redirects to /login if not authenticated
export function AuthGate({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.replace('/');
    }
  }, [loading, user, router]);

  if (loading) return <FullPageLoader message="Verifying your session…" />;
  if (!user) return <FullPageLoader message="Verifying your session…" />;

  return <>{children}</>;
}
