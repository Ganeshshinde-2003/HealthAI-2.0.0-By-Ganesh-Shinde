'use client';

import { Upload, Brain, BarChart3, Lightbulb } from 'lucide-react';

export function HowItWorksSection() {
  const steps = [
    {
      number: '01',
      icon: Upload,
      title: 'Upload Your Data',
      description:
        'Lab reports, symptoms, daily logs, health goals — all formats accepted (PDF, Excel, CSV, text)',
    },
    {
      number: '02',
      icon: Brain,
      title: 'AI Analysis',
      description:
        'Our AI analyzes 50+ biomarkers, identifies patterns, and compares against optimal ranges (not just clinical)',
    },
    {
      number: '03',
      icon: BarChart3,
      title: 'Personalized Insights',
      description:
        'Get your Four Pillars health score (Eat, Sleep, Move, Recover) with root cause analysis',
    },
    {
      number: '04',
      icon: Lightbulb,
      title: 'Clear Action Plan',
      description:
        'Supplement recommendations, lifestyle guidance, and progress tracking tailored to your biology',
    },
  ];

  return (
    <section id="how-it-works" className="py-20 bg-gradient-to-br from-gray-50 to-primary-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
            Turn Health Data Into{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              Health Clarity
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Nova Health combines AI-powered analysis with functional medicine
            principles to give you personalized insights and actionable next
            steps
          </p>
        </div>

        {/* Steps */}
        <div className="relative">
          {/* Connection line */}
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary-200 via-primary-300 to-accent-300 transform -translate-y-1/2"></div>

          <div className="grid md:grid-cols-4 gap-8 relative">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                {/* Step card */}
                <div className="bg-white p-6 rounded-xl shadow-card hover:shadow-card-hover transition-all border border-gray-200 h-full">
                  {/* Step number */}
                  <div className="absolute -top-4 -left-4 w-12 h-12 bg-gradient-primary text-white font-bold text-lg rounded-full flex items-center justify-center shadow-lg">
                    {step.number}
                  </div>

                  {/* Icon */}
                  <div className="mb-4 mt-4 w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center">
                    <step.icon className="w-6 h-6 text-primary" />
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-bold text-gray-900 mb-3">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 text-sm leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <a
            href="/mem/analyze"
            className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-primary text-white text-lg font-semibold rounded-lg shadow-lg hover:shadow-card-hover transition-all transform hover:scale-105"
          >
            Start Your Analysis Now
          </a>
          <p className="mt-4 text-sm text-gray-500">
            No credit card required • Takes 60 seconds
          </p>
        </div>
      </div>
    </section>
  );
}
