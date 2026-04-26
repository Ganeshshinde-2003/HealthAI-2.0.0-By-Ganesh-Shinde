/**
 * ClientWarmUp Component
 *
 * Client-side component that warms up the backend on app load.
 * This component is invisible and only handles the warm-up logic.
 */

'use client';

import { useWarmUp } from '@/hooks/useWarmUp';

export function ClientWarmUp() {
  useWarmUp();
  return null; // This component renders nothing
}
