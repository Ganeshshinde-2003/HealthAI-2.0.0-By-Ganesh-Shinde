'use client';

import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { LoadingAnalysis } from '@/components/LoadingAnalysis';
import { apiClient } from '@/lib/api';
import { AlertCircle } from 'lucide-react';

export default function MonthlyReportPage() {
  const [previousLabReport, setPreviousLabReport] = useState<File | null>(null);
  const [dailyLogs, setDailyLogs] = useState<File | null>(null);
  const [weeklyAssessments, setWeeklyAssessments] = useState<File | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [reportData, setReportData] = useState<any>(null);

  const handleGenerate = async () => {
    if (!previousLabReport || !dailyLogs) {
      alert('Please upload previous lab report and daily logs');
      return;
    }

    setIsGenerating(true);
    setProgress(10);
    setCurrentStep('Uploading files...');
    setError(null);

    try {
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 5, 90));
      }, 1000);

      setCurrentStep('Analyzing monthly trends...');

      const result = await apiClient.generateMonthlyReport(
        previousLabReport,
        dailyLogs,
        weeklyAssessments || undefined
      );

      clearInterval(progressInterval);

      if (result.success && result.data) {
        setReportData(result.data);
        setProgress(100);
        setCurrentStep('Complete!');
      } else {
        throw new Error(result.error || 'Report generation failed');
      }
    } catch (error: any) {
      setError(error.message || 'Failed to generate monthly report');
      setProgress(0);
      setCurrentStep('');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
          📊 Monthly Health Report
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Track your progress over time with comprehensive trend analysis,
          hormonal insights, and behavior pattern tracking.
        </p>
      </div>

      {/* Upload Guide */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          📚 Upload Guide
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📋 Previous Lab Report (Required)
            </h3>
            <p className="text-sm text-gray-600">
              Upload your most recent lab results to track changes from last
              month.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📝 Daily Logs (Required)
            </h3>
            <p className="text-sm text-gray-600">
              Upload your daily tracking data including symptoms, energy,
              sleep, and nutrition.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📊 Weekly Assessments (Optional)
            </h3>
            <p className="text-sm text-gray-600">
              Include weekly check-ins for more comprehensive trend analysis.
            </p>
          </div>
        </div>
      </div>

      {/* File Upload Section */}
      <div className="grid md:grid-cols-3 gap-6">
        <FileUpload
          label="📋 Previous Lab Report"
          description="Upload your most recent lab results"
          multiple={false}
          files={previousLabReport ? [previousLabReport] : []}
          onFilesChange={(files) => setPreviousLabReport(files[0] || null)}
        />
        <FileUpload
          label="📝 Daily Logs"
          description="Upload your daily tracking data"
          multiple={false}
          files={dailyLogs ? [dailyLogs] : []}
          onFilesChange={(files) => setDailyLogs(files[0] || null)}
        />
        <FileUpload
          label="📊 Weekly Assessments"
          description="Upload weekly check-ins (optional)"
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
            className="px-8 py-4 bg-gradient-primary text-white text-lg font-semibold rounded-lg shadow-lg hover:shadow-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
          >
            {isGenerating ? 'Generating...' : 'Generate Monthly Report ✨'}
          </button>
        </div>
      )}

      {/* Loading State */}
      {isGenerating && (
        <LoadingAnalysis progress={progress} currentStep={currentStep} />
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
              onClick={() => setError(null)}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {reportData && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Your Monthly Report
          </h2>
          <pre className="bg-gray-50 p-4 rounded-lg overflow-auto text-sm">
            {JSON.stringify(reportData, null, 2)}
          </pre>
          <div className="mt-6 flex gap-4">
            <button
              onClick={() => {
                setReportData(null);
                setPreviousLabReport(null);
                setDailyLogs(null);
                setWeeklyAssessments(null);
              }}
              className="px-6 py-3 bg-gradient-primary text-white rounded-lg hover:shadow-card-hover transition-all"
            >
              Generate New Report
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
