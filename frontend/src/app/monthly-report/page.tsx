'use client';

import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { LoadingAnalysis } from '@/components/LoadingAnalysis';
import { apiClient } from '@/lib/api';
import { AlertCircle, Download } from 'lucide-react';
import type { MonthlyReportData } from '@/types';
import { downloadJSON } from '@/lib/utils';

export default function MonthlyReportPage() {
  const [previousLabReport, setPreviousLabReport] = useState<File | null>(null);
  const [dailyLogs, setDailyLogs] = useState<File | null>(null);
  const [weeklyAssessments, setWeeklyAssessments] = useState<File | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [reportData, setReportData] = useState<MonthlyReportData | null>(null);

  const handleGenerate = async () => {
    if (!previousLabReport || !dailyLogs) {
      alert('Please upload both lab report and daily logs');
      return;
    }

    setIsGenerating(true);
    setProgress(10);
    setError(null);

    try {
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 5, 90));
      }, 1000);

      const result = await apiClient.generateMonthlyReport(
        previousLabReport,
        dailyLogs,
        weeklyAssessments || undefined
      );

      clearInterval(progressInterval);

      if (result.success && result.data) {
        setProgress(100);
        setReportData(result.data);
        setIsGenerating(false);
      } else {
        throw new Error(result.error || result.message || 'Report generation failed');
      }
    } catch (error: any) {
      setIsGenerating(false);
      setProgress(0);
      setError(error.message || 'Failed to generate monthly report');
    }
  };

  const handleDownload = () => {
    if (reportData) {
      const timestamp = new Date().toISOString().split('T')[0];
      downloadJSON(reportData, `healthai-monthly-report-${timestamp}.json`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
          📊 Monthly Health Reporter
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Track your health journey with comprehensive monthly trend analysis
          and personalized insights.
        </p>
      </div>

      {/* Info Section */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          📚 What to Upload
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              🔬 Previous Lab Report
            </h3>
            <p className="text-sm text-gray-600">
              Your most recent lab test results to track biomarker changes over
              time.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📝 Daily Logs
            </h3>
            <p className="text-sm text-gray-600">
              Daily health logs including symptoms, energy levels, sleep
              quality, and wellness notes.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📋 Weekly Assessments (Optional)
            </h3>
            <p className="text-sm text-gray-600">
              Weekly check-ins, goal progress, and behavior tracking data.
            </p>
          </div>
        </div>
      </div>

      {/* File Upload Section */}
      <div className="grid md:grid-cols-3 gap-6">
        <FileUpload
          label="🔬 Previous Lab Report"
          description="Upload your latest lab test results"
          multiple={false}
          files={previousLabReport ? [previousLabReport] : []}
          onFilesChange={(files) => setPreviousLabReport(files[0] || null)}
        />
        <FileUpload
          label="📝 Daily Logs (Required)"
          description="Upload your daily health tracking logs"
          multiple={false}
          files={dailyLogs ? [dailyLogs] : []}
          onFilesChange={(files) => setDailyLogs(files[0] || null)}
        />
        <FileUpload
          label="📋 Weekly Assessments"
          description="Upload weekly check-ins and assessments"
          multiple={false}
          files={weeklyAssessments ? [weeklyAssessments] : []}
          onFilesChange={(files) => setWeeklyAssessments(files[0] || null)}
        />
      </div>

      {/* Generate Button */}
      {!reportData && (
        <div className="text-center">
          <button
            onClick={handleGenerate}
            disabled={!previousLabReport || !dailyLogs || isGenerating}
            className="px-8 py-4 bg-primary-600 text-white text-lg font-semibold rounded-lg shadow-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
          >
            {isGenerating ? 'Generating...' : 'Generate Monthly Report ✨'}
          </button>
        </div>
      )}

      {/* Loading State */}
      {isGenerating && (
        <LoadingAnalysis
          progress={progress}
          currentStep="Analyzing your monthly health trends..."
        />
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-start gap-4">
          <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900 mb-2">
              Report Generation Failed
            </h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={() => {
                setError(null);
                setProgress(0);
              }}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {reportData && (
        <div className="space-y-6 animate-slide-up">
          {/* Header */}
          <div className="bg-green-50 border border-green-200 rounded-xl p-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-green-900 mb-2">
                  ✨ Monthly Report Generated!
                </h2>
                <p className="text-green-700">
                  Review your monthly health trends and insights below.
                </p>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 px-4 py-2 bg-white border border-green-300 text-green-700 rounded-lg hover:bg-green-50 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download Report
                </button>
                <button
                  onClick={() => {
                    setReportData(null);
                    setPreviousLabReport(null);
                    setDailyLogs(null);
                    setWeeklyAssessments(null);
                  }}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  New Report
                </button>
              </div>
            </div>
          </div>

          {/* Month Summary */}
          {reportData.month_summary && (
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <h3 className="text-2xl font-semibold text-gray-900 mb-4">
                📅 {reportData.month_summary.month} Summary
              </h3>

              <div className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-2">
                    Overall Trend
                  </h4>
                  <p className="text-gray-700">
                    {reportData.month_summary.overall_trend}
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  {reportData.month_summary.key_improvements.length > 0 && (
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">
                        ✅ Key Improvements
                      </h4>
                      <ul className="space-y-1">
                        {reportData.month_summary.key_improvements.map(
                          (improvement, idx) => (
                            <li
                              key={idx}
                              className="text-sm text-gray-700 flex items-start gap-2"
                            >
                              <span className="text-green-600">→</span>
                              {improvement}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}

                  {reportData.month_summary.key_concerns.length > 0 && (
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">
                        ⚠️ Areas of Focus
                      </h4>
                      <ul className="space-y-1">
                        {reportData.month_summary.key_concerns.map(
                          (concern, idx) => (
                            <li
                              key={idx}
                              className="text-sm text-gray-700 flex items-start gap-2"
                            >
                              <span className="text-yellow-600">→</span>
                              {concern}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Full JSON Data */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              📋 Complete Report Data
            </h3>
            <div className="bg-gray-50 rounded-lg p-4 overflow-auto max-h-96 scrollbar-thin">
              <pre className="text-sm text-gray-700">
                {JSON.stringify(reportData, null, 2)}
              </pre>
            </div>
          </div>

          {/* Disclaimer */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-900">
              <span className="font-semibold">⚠️ Medical Disclaimer:</span> This
              report is for informational purposes only. Always consult with a
              qualified healthcare provider for medical advice and treatment.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
