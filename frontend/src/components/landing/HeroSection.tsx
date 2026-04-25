'use client';

import Link from 'next/link';
import { ArrowRight, Shield, Sparkles, Activity, CheckCircle } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-accent-50 py-20 md:py-32">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full opacity-20 blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-200 rounded-full opacity-20 blur-3xl"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left column - Text content */}
          <div className="space-y-8 animate-fade-in">
            {/* Brand badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-primary-200 rounded-full shadow-sm">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-primary">
                Nova Health
              </span>
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight">
              Your Personal{' '}
              <span className="bg-gradient-primary bg-clip-text text-transparent">
                Health Intelligence
              </span>{' '}
              Layer
            </h1>

            {/* Subheadline */}
            <p className="text-xl text-gray-600 leading-relaxed">
              Turn lab reports and health data into clear, personalized action
              plans with AI-powered biomarker analysis, lifestyle scoring, and
              behavior-guided recommendations.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/mem/analyze"
                className="group inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-primary text-white text-lg font-semibold rounded-lg shadow-lg hover:shadow-card-hover transition-all transform hover:scale-105"
              >
                Start Your Free Analysis
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <button
                onClick={() => {
                  document
                    .getElementById('how-it-works')
                    ?.scrollIntoView({ behavior: 'smooth' });
                }}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-primary border-2 border-primary text-lg font-semibold rounded-lg hover:bg-primary-50 transition-all"
              >
                See How It Works
              </button>
            </div>

            {/* Trust Indicators */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8">
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-primary" />
                <span className="text-sm font-medium text-gray-700">
                  HIPAA Compliant
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <span className="text-sm font-medium text-gray-700">
                  Google Vertex AI
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-primary" />
                <span className="text-sm font-medium text-gray-700">
                  50+ Biomarkers
                </span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-primary" />
                <span className="text-sm font-medium text-gray-700">
                  Evidence-Based
                </span>
              </div>
            </div>
          </div>

          {/* Right column - Visual/Dashboard preview */}
          <div className="relative animate-slide-up">
            <div className="relative bg-white rounded-2xl shadow-2xl p-6 border border-gray-200">
              {/* Dashboard Preview */}
              <div className="space-y-4">
                {/* Header */}
                <div className="flex items-center justify-between pb-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Health Dashboard
                  </h3>
                  <span className="px-3 py-1 bg-success-50 text-success-600 text-sm font-medium rounded-full">
                    Optimal
                  </span>
                </div>

                {/* Biomarker Cards */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-success-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">
                      HDL Cholesterol
                    </span>
                    <span className="text-sm font-bold text-success-600">
                      75 mg/dL
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-warning-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">
                      Vitamin D
                    </span>
                    <span className="text-sm font-bold text-warning-600">
                      28 ng/mL
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-success-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">
                      Hemoglobin A1c
                    </span>
                    <span className="text-sm font-bold text-success-600">
                      5.2%
                    </span>
                  </div>
                </div>

                {/* Four Pillars */}
                <div className="pt-4 border-t border-gray-200">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">
                    Four Pillars Score
                  </h4>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="text-center p-3 bg-primary-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary">8</div>
                      <div className="text-xs text-gray-600">Eat Well</div>
                    </div>
                    <div className="text-center p-3 bg-primary-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary">7</div>
                      <div className="text-xs text-gray-600">Sleep Well</div>
                    </div>
                    <div className="text-center p-3 bg-primary-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary">9</div>
                      <div className="text-xs text-gray-600">Move Well</div>
                    </div>
                    <div className="text-center p-3 bg-primary-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary">6</div>
                      <div className="text-xs text-gray-600">Recover Well</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating badge */}
              <div className="absolute -top-4 -right-4 px-4 py-2 bg-gradient-primary text-white text-sm font-semibold rounded-full shadow-lg">
                AI-Powered
              </div>
            </div>

            {/* Decorative elements */}
            <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-accent-200 rounded-full opacity-40 blur-2xl"></div>
            <div className="absolute -top-6 -right-6 w-32 h-32 bg-primary-200 rounded-full opacity-40 blur-2xl"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
