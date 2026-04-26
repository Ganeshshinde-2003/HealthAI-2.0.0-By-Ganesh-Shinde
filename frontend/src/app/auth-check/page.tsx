'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { FullPageLoader } from '@/components/FullPageLoader';

export default function AuthCheckPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;
    if (user) {
      router.replace('/mem/analyze');
    } else {
      router.replace('/login');
    }
  }, [loading, user, router]);

  return <FullPageLoader />;
}
