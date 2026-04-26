'use client';

import { Suspense } from 'react';
import { FullPageLoader } from '@/components/FullPageLoader';
import VerifyEmailContent from './VerifyEmailContent';

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<FullPageLoader />}>
      <VerifyEmailContent />
    </Suspense>
  );
}
