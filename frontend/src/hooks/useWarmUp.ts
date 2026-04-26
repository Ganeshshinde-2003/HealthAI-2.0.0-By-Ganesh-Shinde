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

export function useWarmUp() {
  const hasWarmedUp = useRef(false);

  useEffect(() => {
    // Only warm up once per session
    if (hasWarmedUp.current) return;

    const warmUpBackend = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

        console.log('🔥 Warming up backend...');

        // Call warm-up endpoint
        const response = await fetch(`${apiUrl}/warmup`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();

          if (data.database === 'connected') {
            console.log('✅ Backend & Database ready!');
          } else {
            console.log('⚡ Backend ready (Database warming up...)');
          }
        } else {
          console.log('⏳ Backend starting...');
        }

        hasWarmedUp.current = true;
      } catch (error) {
        // Silently fail - backend is probably just starting up
        console.log('🔄 Services warming up in background...');
        hasWarmedUp.current = true;
      }
    };

    // Start warm-up immediately
    warmUpBackend();
  }, []);
}
