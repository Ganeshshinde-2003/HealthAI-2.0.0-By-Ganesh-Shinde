'use client';

import { Activity, Heart, TrendingUp, Pill, Target, Lock } from 'lucide-react';

export function FeaturesSection() {
  const features = [
    {
      icon: Activity,
      title: 'Comprehensive Biomarker Analysis',
      description:
        'Deep analysis of 50+ biomarkers including hormones, thyroid, vitamins, metabolic markers, and inflammatory indicators. Get optimal ranges, not just clinical ranges.',
      color: 'text-primary',
      bgColor: 'bg-primary-50',
    },
    {
      icon: Heart,
      title: 'Four Pillars Health Score',
      description:
        'Personalized scoring for Eat Well, Sleep Well, Move Well, and Recover Well based on your biomarkers and lifestyle data.',
      color: 'text-danger',
      bgColor: 'bg-danger-50',
    },
    {
      icon: TrendingUp,
      title: 'Monthly Progress Reports',
      description:
        'Track trends over time with radar charts, hormonal insights, and behavior pattern analysis. See what\'s working and what needs adjustment.',
      color: 'text-success',
      bgColor: 'bg-success-50',
    },
    {
      icon: Pill,
      title: 'Smart Supplement Recommendations',
      description:
        'Evidence-based supplement suggestions with specific dosages, timing, and cautions based on your unique deficiencies and goals.',
      color: 'text-warning',
      bgColor: 'bg-warning-50',
    },
    {
      icon: Target,
      title: 'Root Cause Analysis',
      description:
        'Understand the "why" behind your symptoms and biomarkers. Connect the dots between diet, sleep, stress, and lab results.',
      color: 'text-info',
      bgColor: 'bg-info-50',
    },
    {
      icon: Lock,
      title: 'Privacy First',
      description:
        'HIPAA-compliant processing, no data storage, encrypted connections. Your health data stays private and secure.',
      color: 'text-gray-700',
      bgColor: 'bg-gray-100',
    },
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
            Everything You Need in{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              One Place
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Powerful features designed to turn complex health data into clear,
            actionable insights
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-8 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-card transition-all"
            >
              <div
                className={`mb-6 w-14 h-14 ${feature.bgColor} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}
              >
                <feature.icon className={`w-7 h-7 ${feature.color}`} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-4 px-8 py-4 bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl border border-primary-200">
            <div>
              <p className="text-sm font-semibold text-primary mb-1">
                Ready to get started?
              </p>
              <p className="text-xs text-gray-600">
                Upload your first lab report and see the difference
              </p>
            </div>
            <a
              href="/auth-check"
              className="px-6 py-3 bg-gradient-primary text-white font-semibold rounded-lg hover:shadow-card-hover transition-all whitespace-nowrap"
            >
              Try It Free
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
