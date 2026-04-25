'use client';

import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { AnalysisResults } from '@/components/AnalysisResults';
import { LoadingAnalysis } from '@/components/LoadingAnalysis';
import { apiClient } from '@/lib/api';
import type { AnalysisResult, AnalysisState } from '@/types';
import { AlertCircle } from 'lucide-react';

export default function HealthAnalyzerPage() {
  const [labReports, setLabReports] = useState<File[]>([]);
  const [healthAssessment, setHealthAssessment] = useState<File | null>(null);
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    isAnalyzing: false,
    progress: 0,
    currentStep: '',
  });

  const handleAnalyze = async () => {
    if (labReports.length === 0) {
      alert('Please upload at least one lab report');
      return;
    }

    setAnalysisState({
      isAnalyzing: true,
      progress: 10,
      currentStep: 'Uploading files...',
    });

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setAnalysisState((prev) => ({
          ...prev,
          progress: Math.min(prev.progress + 5, 90),
        }));
      }, 1000);

      setAnalysisState((prev) => ({
        ...prev,
        progress: 20,
        currentStep: 'Analyzing biomarkers...',
      }));

      const result = await apiClient.analyzeHealth(
        labReports,
        healthAssessment || undefined
      );

      clearInterval(progressInterval);

      console.log('🔍 API Response:', result);
      console.log('🔍 Success?', result.success);
      console.log('🔍 Data:', result.data);

      if (result.success && result.data) {
        console.log('✅ Setting state with data:', result.data);
        setAnalysisState({
          isAnalyzing: false,
          progress: 100,
          currentStep: 'Complete!',
          result: result.data,
        });
      } else {
        console.error('❌ No data in response');
        throw new Error(result.error || 'Analysis failed');
      }
    } catch (error: any) {
      setAnalysisState({
        isAnalyzing: false,
        progress: 0,
        currentStep: '',
        error: error.message || 'Failed to analyze health data',
      });
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
          🌿 Your Personal AI Health Assistant
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Upload your health data for personalized AI-powered analysis with
          comprehensive biomarker insights and actionable recommendations.
        </p>
      </div>

      {/* Upload Guide */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          📚 Upload Guide
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              🔬 Lab Reports (Required)
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              We analyze 50+ biomarkers including hormones, thyroid, vitamins,
              metabolic markers, and inflammatory markers.
            </p>
            <p className="text-sm text-gray-500">
              Accepted formats: PDF, Word, Excel, CSV, Plain Text (Max 10MB)
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 mb-2">
              📝 Health Data (Optional)
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              Include symptoms, health goals, current medications, lifestyle
              habits, or any health concerns for more personalized
              recommendations.
            </p>
            <p className="text-sm text-gray-500">
              The more context you provide, the better your recommendations!
            </p>
          </div>
        </div>
      </div>

      {/* File Upload Section */}
      <div className="grid md:grid-cols-2 gap-6">
        <FileUpload
          label="📋 Lab Reports (Required)"
          description="Upload your blood test results, hormone panels, or medical lab reports"
          multiple
          files={labReports}
          onFilesChange={setLabReports}
        />
        <FileUpload
          label="📝 Health Data (Optional)"
          description="Upload your health information, symptoms, goals, or medical history"
          multiple={false}
          files={healthAssessment ? [healthAssessment] : []}
          onFilesChange={(files) => setHealthAssessment(files[0] || null)}
        />
      </div>

      {/* Analyze Button */}
      {!analysisState.result && (
        <div className="text-center">
          <button
            onClick={handleAnalyze}
            disabled={labReports.length === 0 || analysisState.isAnalyzing}
            className="px-8 py-4 bg-primary-600 text-white text-lg font-semibold rounded-lg shadow-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
          >
            {analysisState.isAnalyzing ? 'Analyzing...' : 'Analyze My Data ✨'}
          </button>
        </div>
      )}

      {/* Loading State */}
      {analysisState.isAnalyzing && (
        <LoadingAnalysis
          progress={analysisState.progress}
          currentStep={analysisState.currentStep}
        />
      )}

      {/* Error State */}
      {analysisState.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-start gap-4">
          <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900 mb-2">Analysis Failed</h3>
            <p className="text-red-700">{analysisState.error}</p>
            <button
              onClick={() =>
                setAnalysisState({
                  isAnalyzing: false,
                  progress: 0,
                  currentStep: '',
                })
              }
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {(() => {
        console.log('🎯 Current analysisState.result:', analysisState.result);
        console.log('🎯 Should render results?', !!analysisState.result);
        return analysisState.result && (
          <AnalysisResults
            data={analysisState.result}
            onNewAnalysis={() => {
              setAnalysisState({
                isAnalyzing: false,
                progress: 0,
                currentStep: '',
              });
              setLabReports([]);
              setHealthAssessment(null);
            }}
          />
        );
      })()}
    </div>
  );
}
