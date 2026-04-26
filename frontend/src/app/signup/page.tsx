'use client';

import { useState, useEffect, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Eye, EyeOff, Mail, Lock, User, Sparkles,
  ArrowRight, AlertCircle, CheckCircle2, Check,
} from 'lucide-react';
import { apiSignup } from '@/lib/authApi';
import { useAuth } from '@/context/AuthContext';

const PASSWORD_RULES = [
  { label: 'At least 8 characters', test: (p: string) => p.length >= 8 },
  { label: 'One uppercase letter',  test: (p: string) => /[A-Z]/.test(p) },
  { label: 'One lowercase letter',  test: (p: string) => /[a-z]/.test(p) },
  { label: 'One number',            test: (p: string) => /\d/.test(p) },
];

export default function SignupPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    if (!authLoading && user) {
      router.replace('/mem/analyze');
    }
  }, [authLoading, user, router]);

  const [name, setName]                   = useState('');
  const [email, setEmail]                 = useState('');
  const [password, setPassword]           = useState('');
  const [confirm, setConfirm]             = useState('');
  const [showPassword, setShowPassword]   = useState(false);
  const [showConfirm, setShowConfirm]     = useState(false);
  const [agreed, setAgreed]               = useState(false);
  const [loading, setLoading]             = useState(false);
  const [error, setError]                 = useState('');
  const [success, setSuccess]             = useState('');
  const [passwordFocused, setPasswordFocused] = useState(false);

  const allRulesPassed = PASSWORD_RULES.every((r) => r.test(password));
  const passwordsMatch = password === confirm && confirm.length > 0;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');

    if (!allRulesPassed) {
      setError('Please meet all password requirements.');
      return;
    }
    if (!passwordsMatch) {
      setError('Passwords do not match.');
      return;
    }
    if (!agreed) {
      setError('Please accept the terms and conditions.');
      return;
    }

    setLoading(true);
    try {
      const message = await apiSignup(name.trim(), email.trim().toLowerCase(), password);
      setSuccess(message);
    } catch (err: any) {
      setError(err.message?.replace('API Error: ', '') || 'Signup failed.');
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-6">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-card border border-gray-100 p-10 text-center animate-fade-in">
          <div className="w-16 h-16 bg-success-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 className="w-8 h-8 text-success-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Check your email</h2>
          <p className="text-gray-500 text-sm leading-relaxed mb-8">{success}</p>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-md hover:shadow-card-hover transition-all transform hover:scale-[1.02]"
          >
            Back to Sign In <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex">
      {/* ── Left panel ─────────────────────────────────────────────────────── */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-primary relative overflow-hidden flex-col justify-between p-12">
        <div className="absolute -top-20 -left-20 w-72 h-72 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-20 -right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl" />

        {/* Logo */}
        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-white text-xl font-bold">Nova Health</span>
        </div>

        {/* Copy */}
        <div className="relative space-y-6">
          <h2 className="text-4xl font-bold text-white leading-tight">
            Start your journey<br />to better health.
          </h2>
          <p className="text-white/80 text-lg leading-relaxed">
            Join thousands who use Nova Health to understand their biomarkers
            and take control of their wellness.
          </p>

          {/* What you get */}
          <div className="space-y-3 pt-2">
            {[
              'AI-powered biomarker analysis',
              'Personalised action plans',
              'Monthly progress reports',
              'Secure, HIPAA-compliant storage',
            ].map((item) => (
              <div key={item} className="flex items-center gap-3">
                <div className="w-5 h-5 bg-white/20 rounded-full flex items-center justify-center shrink-0">
                  <Check className="w-3 h-3 text-white" />
                </div>
                <span className="text-white/85 text-sm">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="relative text-white/50 text-sm">
          &ldquo;An ounce of prevention is worth a pound of cure.&rdquo;
        </p>
      </div>

      {/* ── Right panel ────────────────────────────────────────────────────── */}
      <div className="flex-1 flex items-center justify-center px-6 py-12 bg-gray-50 overflow-y-auto">
        <div className="w-full max-w-md animate-slide-up">

          {/* Mobile logo */}
          <div className="flex lg:hidden items-center gap-2 mb-8">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="text-gray-900 text-lg font-bold">Nova Health</span>
          </div>

          <div className="bg-white rounded-2xl shadow-card border border-gray-100 p-8">
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
              <p className="text-gray-500 mt-1 text-sm">Start your free health analysis today</p>
            </div>

            {error && (
              <div className="mb-6 flex items-start gap-3 p-4 bg-danger-50 border border-danger-200 rounded-xl text-danger-700 text-sm animate-fade-in">
                <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5" noValidate>
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Full name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    autoComplete="name"
                    placeholder="Jane Smith"
                    className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Email address</label>
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
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onFocus={() => setPasswordFocused(true)}
                    onBlur={() => setPasswordFocused(false)}
                    required
                    autoComplete="new-password"
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

                {/* Password strength checklist */}
                {(passwordFocused || password.length > 0) && (
                  <div className="mt-3 grid grid-cols-2 gap-1.5 animate-fade-in">
                    {PASSWORD_RULES.map((rule) => {
                      const passed = rule.test(password);
                      return (
                        <div key={rule.label} className="flex items-center gap-1.5">
                          <div className={`w-3.5 h-3.5 rounded-full flex items-center justify-center transition-colors ${passed ? 'bg-success-500' : 'bg-gray-200'}`}>
                            {passed && <Check className="w-2 h-2 text-white" />}
                          </div>
                          <span className={`text-xs transition-colors ${passed ? 'text-success-600' : 'text-gray-400'}`}>
                            {rule.label}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Confirm password */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Confirm password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showConfirm ? 'text' : 'password'}
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    required
                    autoComplete="new-password"
                    placeholder="••••••••"
                    className={`w-full pl-10 pr-10 py-3 border rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all ${
                      confirm.length > 0
                        ? passwordsMatch
                          ? 'border-success-300 bg-success-50/30'
                          : 'border-danger-300 bg-danger-50/30'
                        : 'border-gray-200'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirm((v) => !v)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    tabIndex={-1}
                  >
                    {showConfirm ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Terms */}
              <label className="flex items-start gap-3 cursor-pointer group">
                <div className={`mt-0.5 w-4 h-4 rounded border-2 flex items-center justify-center shrink-0 transition-colors ${agreed ? 'bg-primary border-primary' : 'border-gray-300 group-hover:border-primary'}`}>
                  {agreed && <Check className="w-2.5 h-2.5 text-white" />}
                  <input
                    type="checkbox"
                    checked={agreed}
                    onChange={(e) => setAgreed(e.target.checked)}
                    className="sr-only"
                  />
                </div>
                <span className="text-sm text-gray-600 leading-tight">
                  I agree to the{' '}
                  <Link href="/terms" className="text-primary hover:underline font-medium">Terms of Service</Link>
                  {' '}and{' '}
                  <Link href="/privacy" className="text-primary hover:underline font-medium">Privacy Policy</Link>
                </span>
              </label>

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
                    Create Account
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <p className="mt-6 text-center text-sm text-gray-500">
              Already have an account?{' '}
              <Link href="/login" className="text-primary font-semibold hover:underline">
                Sign in
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
