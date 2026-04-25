'use client';

import { FileQuestion, Shuffle, TrendingDown } from 'lucide-react';

export function ProblemSection() {
  const problems = [
    {
      icon: FileQuestion,
      title: 'You Have Reports, Not Answers',
      description:
        'Lab results with numbers and ranges, but no clear explanation of what matters or what to do next.',
    },
    {
      icon: Shuffle,
      title: 'Generic Advice Doesn\'t Work',
      description:
        'One-size-fits-all recommendations that ignore your unique biology, lifestyle, and health goals.',
    },
    {
      icon: TrendingDown,
      title: 'Progress is Hard to Track',
      description:
        'Fragmented tools across apps and spreadsheets with no way to see if you\'re actually improving over time.',
    },
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
            Your Health Data Shouldn't Be a{' '}
            <span className="text-primary">Mystery</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Most people struggle with the same health data challenges
          </p>
        </div>

        {/* Problem Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          {problems.map((problem, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-xl shadow-card hover:shadow-card-hover transition-all border border-gray-200 group"
            >
              <div className="mb-6 w-14 h-14 bg-gradient-primary rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <problem.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                {problem.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {problem.description}
              </p>
            </div>
          ))}
        </div>

        {/* Visual comparison */}
        <div className="mt-16 bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            {/* Before */}
            <div className="space-y-4">
              <div className="inline-block px-4 py-2 bg-danger-50 text-danger-600 rounded-full text-sm font-semibold">
                Before Nova Health
              </div>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-danger-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Confusing lab reports with no context
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-danger-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Googling symptoms and getting overwhelmed
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-danger-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    No way to track progress over time
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-danger-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Generic supplement recommendations
                  </p>
                </div>
              </div>
            </div>

            {/* After */}
            <div className="space-y-4">
              <div className="inline-block px-4 py-2 bg-success-50 text-success-600 rounded-full text-sm font-semibold">
                With Nova Health
              </div>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-success-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Clear explanations of every biomarker
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-success-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Personalized action plans based on your data
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-success-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Monthly trend analysis and progress tracking
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-success-500 rounded-full mt-2"></div>
                  <p className="text-gray-600">
                    Evidence-based supplements with dosing
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
