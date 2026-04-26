'use client';

import { useState, useEffect, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Eye, EyeOff, Mail, Lock, Sparkles, Activity,
  Shield, CheckCircle, ArrowRight, AlertCircle,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const router = useRouter();
  const { login, user, loading: authLoading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Already logged in → go straight to the app
  useEffect(() => {
    if (!authLoading && user) {
      router.replace('/mem/analyze');
    }
  }, [authLoading, user, router]);

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary rounded-full animate-spin" />
          <p className="text-gray-500 text-sm">Loading…</p>
        </div>
      </div>
    );
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email.trim().toLowerCase(), password);
      router.push('/mem/analyze');
    } catch (err: any) {
      setError(err.message?.replace('API Error: ', '') || 'Login failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* ── Left panel ─────────────────────────────────────────────────────── */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-primary relative overflow-hidden flex-col justify-between p-12">
        {/* Blurred blobs */}
        <div className="absolute -top-20 -left-20 w-72 h-72 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-20 -right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl" />

        {/* Logo */}
        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-white text-xl font-bold">Nova Health</span>
        </div>

        {/* Centre copy */}
        <div className="relative space-y-6">
          <h2 className="text-4xl font-bold text-white leading-tight">
            Your health journey<br />continues here.
          </h2>
          <p className="text-white/80 text-lg leading-relaxed">
            Access your AI-powered health dashboard, biomarker analysis,
            and personalised action plans.
          </p>

          {/* Mini stat cards */}
          <div className="grid grid-cols-2 gap-4 pt-4">
            {[
              { icon: Activity, label: 'Biomarkers tracked', value: '50+' },
              { icon: Shield,   label: 'Data security',      value: 'HIPAA' },
              { icon: CheckCircle, label: 'Evidence-based',  value: '100%' },
              { icon: Sparkles,  label: 'AI powered',        value: 'Gemini' },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <Icon className="w-5 h-5 text-white/70 mb-2" />
                <div className="text-white font-bold text-lg">{value}</div>
                <div className="text-white/60 text-xs">{label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer quote */}
        <p className="relative text-white/50 text-sm">
          &ldquo;Prevention is better than cure.&rdquo;
        </p>
      </div>

      {/* ── Right panel ────────────────────────────────────────────────────── */}
      <div className="flex-1 flex items-center justify-center px-6 py-12 bg-gray-50">
        <div className="w-full max-w-md animate-fade-in">

          {/* Mobile logo */}
          <div className="flex lg:hidden items-center gap-2 mb-8">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="text-gray-900 text-lg font-bold">Nova Health</span>
          </div>

          <div className="bg-white rounded-2xl shadow-card border border-gray-100 p-8">
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
              <p className="text-gray-500 mt-1 text-sm">Sign in to your account to continue</p>
            </div>

            {error && (
              <div className="mb-6 flex items-start gap-3 p-4 bg-danger-50 border border-danger-200 rounded-xl text-danger-700 text-sm animate-fade-in">
                <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5" noValidate>
              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Email address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                    placeholder="you@example.com"
                    className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-sm font-medium text-gray-700">Password</label>
                  <Link href="/forgot-password" className="text-xs text-primary hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((v) => !v)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="group w-full flex items-center justify-center gap-2 py-3 px-6 bg-gradient-primary text-white font-semibold rounded-xl shadow-md hover:shadow-card-hover transition-all transform hover:scale-[1.02] disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? (
                  <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    Sign In
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <p className="mt-6 text-center text-sm text-gray-500">
              Don&apos;t have an account?{' '}
              <Link href="/signup" className="text-primary font-semibold hover:underline">
                Create one
              </Link>
            </p>
          </div>

          <p className="mt-6 text-center text-xs text-gray-400">
            Protected by end-to-end encryption &middot; HIPAA compliant
          </p>
        </div>
      </div>
    </div>
  );
}
