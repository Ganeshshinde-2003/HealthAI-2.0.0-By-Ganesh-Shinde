import Link from 'next/link';

export default function MemLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
              <span className="text-3xl">🌿</span>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Nova Health
                </h1>
                <p className="text-sm text-gray-600">
                  Your Personal Health Intelligence Layer
                </p>
              </div>
            </Link>
            <nav className="hidden md:flex items-center gap-6">
              <Link
                href="/"
                className="text-gray-700 hover:text-primary font-medium transition-colors"
              >
                Home
              </Link>
              <Link
                href="/mem/analyze"
                className="text-gray-700 hover:text-primary font-medium transition-colors"
              >
                Health Analyzer
              </Link>
              <Link
                href="/mem/monthly"
                className="text-gray-700 hover:text-primary font-medium transition-colors"
              >
                Monthly Report
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">
                Nova Health
              </h3>
              <p className="text-sm text-gray-600">
                AI-powered personal health intelligence for precision wellness
                and biomarker analysis.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Features</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>🔬 Comprehensive Biomarker Analysis</li>
                <li>💪 Four Pillars Framework</li>
                <li>📊 Monthly Health Reports</li>
                <li>💊 Smart Supplement Recommendations</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Important</h3>
              <p className="text-sm text-gray-600">
                ⚠️ This application is for educational purposes. Always consult
                a licensed healthcare provider for medical decisions.
              </p>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-gray-600">
            <p>
              &copy; {new Date().getFullYear()} Nova Health. All rights
              reserved.
            </p>
            <p className="mt-2">Version 2.0.0 | Powered by Google Vertex AI</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
