'use client';

interface LoadingAnalysisProps {
  progress: number;
  currentStep: string;
}

export function LoadingAnalysis({
  progress,
  currentStep,
}: LoadingAnalysisProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200 animate-slide-up">
      <div className="text-center space-y-6">
        <div className="flex justify-center">
          <div className="spinner"></div>
        </div>

        <div className="space-y-2">
          <h3 className="text-2xl font-semibold text-gray-900">
            Analyzing Your Health Data
          </h3>
          <p className="text-gray-600">{currentStep}</p>
        </div>

        <div className="w-full max-w-md mx-auto">
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-2">{progress}% Complete</p>
        </div>

        <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto pt-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl mb-2">🔬</div>
            <p className="text-sm font-medium text-gray-700">Biomarkers</p>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl mb-2">💪</div>
            <p className="text-sm font-medium text-gray-700">Four Pillars</p>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl mb-2">💊</div>
            <p className="text-sm font-medium text-gray-700">Supplements</p>
          </div>
        </div>

        <p className="text-sm text-gray-500 italic">
          This typically takes 30-60 seconds. Our AI is analyzing your data
          with precision...
        </p>
      </div>
    </div>
  );
}
