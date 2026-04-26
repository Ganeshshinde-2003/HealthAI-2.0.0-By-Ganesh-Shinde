/**
 * useWarmUp Hook
 *
 * Warms up the backend server and database to eliminate cold starts.
 * Called automatically when user visits the app.
 *
 * This ensures:
 * - Backend server (Render) is awake
 * - Database (Neon) is connected
 * - First API call is fast with no delay
 */

'use client';

import { useEffect, useRef } from 'react';
import { apiClient } from '@/lib/api';
import axios from 'axios';

export function useWarmUp() {
  const hasWarmedUp = useRef(false);

  useEffect(() => {
    // Only warm up once per session
    if (hasWarmedUp.current) return;

    const warmUpBackend = async () => {
      try {
        console.log('🔥 Warming up backend...');

        // Call warm-up endpoint using axios directly
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api'}/warmup`,
          {
            timeout: 10000,
          }
        );

        const data = response.data;

        if (data.database === 'connected') {
          console.log('✅ Backend & Database ready!');
        } else {
          console.log('⚡ Backend ready (Database: ' + data.database + ')');
        }

        hasWarmedUp.current = true;
      } catch (error) {
        // Silently fail - backend is probably just starting up
        if (axios.isAxiosError(error)) {
          console.log('⏳ Backend warming up... (' + error.message + ')');
        } else {
          console.log('🔄 Services warming up in background...');
        }
        hasWarmedUp.current = true;
      }
    };

    // Start warm-up immediately
    warmUpBackend();
  }, []);
}
