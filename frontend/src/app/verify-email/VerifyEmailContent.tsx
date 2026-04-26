'use client';

import { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle2, XCircle, Sparkles, Loader2 } from 'lucide-react';
import axios from 'axios';

type Status = 'loading' | 'success' | 'error';

export default function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [status, setStatus] = useState<Status>('loading');
  const [message, setMessage] = useState('');
  const called = useRef(false);

  useEffect(() => {
    if (called.current) return;
    called.current = true;

    if (!token) {
      setStatus('error');
      setMessage('No verification token found in the link.');
      return;
    }

    const verify = async () => {
      try {
        const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
        const res = await axios.get(`${base}/auth/verify-email`, { params: { token } });
        setMessage(res.data.message || 'Email verified successfully!');
        setStatus('success');
      } catch (err: any) {
        const msg = err?.response?.data?.error || 'Verification failed. The link may have expired.';
        setMessage(msg);
        setStatus('error');
      }
    };

    verify();
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-6">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-card border border-gray-100 p-10 text-center animate-fade-in">
        {/* Logo */}
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-9 h-9 bg-gradient-primary rounded-xl flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="text-gray-900 text-lg font-bold">Nova Health</span>
        </div>

        {status === 'loading' && (
          <>
            <Loader2 className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
            <h2 className="text-xl font-bold text-gray-900 mb-2">Verifying your email…</h2>
            <p className="text-gray-500 text-sm">Just a moment, please.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-16 h-16 bg-success-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle2 className="w-8 h-8 text-success-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Email verified!</h2>
            <p className="text-gray-500 text-sm mb-8">{message}</p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-md hover:shadow-card-hover transition-all transform hover:scale-[1.02]"
            >
              Sign in to your account
            </Link>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="w-16 h-16 bg-danger-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <XCircle className="w-8 h-8 text-danger" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Verification failed</h2>
            <p className="text-gray-500 text-sm mb-8">{message}</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link
                href="/signup"
                className="px-6 py-3 border-2 border-primary text-primary font-semibold rounded-xl hover:bg-primary-50 transition-all"
              >
                Sign up again
              </Link>
              <Link
                href="/login"
                className="px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-md hover:shadow-card-hover transition-all"
              >
                Back to login
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
