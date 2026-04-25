'use client';

import { useState } from 'react';
import { Download, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import type { AnalysisResult } from '@/types';
import {
  downloadJSON,
  getStatusColor,
  getPriorityColor,
  getPillarScoreColor,
} from '@/lib/utils';

interface AnalysisResultsProps {
  data: AnalysisResult;
  onNewAnalysis: () => void;
}

export function AnalysisResults({ data, onNewAnalysis }: AnalysisResultsProps) {
  const [expandedSections, setExpandedSections] = useState<{
    [key: string]: boolean;
  }>({
    biomarkers: true,
    pillars: true,
    supplements: true,
  });

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleDownload = () => {
    const timestamp = new Date().toISOString().split('T')[0];
    downloadJSON(data, `healthai-analysis-${timestamp}.json`);
  };

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Header with Actions */}
      <div className="bg-green-50 border border-green-200 rounded-xl p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-green-900 mb-2">
              ✨ Analysis Complete!
            </h2>
            <p className="text-green-700">
              Your personalized health insights are ready. Review the results
              below.
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-green-300 text-green-700 rounded-lg hover:bg-green-50 transition-colors"
            >
              <Download className="w-4 h-4" />
              Download JSON
            </button>
            <button
              onClick={onNewAnalysis}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Biomarker Analysis */}
      {data.lab_analysis && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">
          <button
            onClick={() => toggleSection('biomarkers')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-gray-900">
              🔬 Biomarker Analysis ({data.lab_analysis.biomarkers_tested_count}{' '}
              markers)
            </h3>
            {expandedSections.biomarkers ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>

          {expandedSections.biomarkers && (
            <div className="px-6 pb-6 space-y-4">
              {/* Summary */}
              {data.lab_analysis.biomarker_categories_summary && (
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-3xl font-bold text-green-600">
                      {data.lab_analysis.biomarker_categories_summary.optimal_count || 0}
                    </p>
                    <p className="text-sm text-green-700 font-medium">
                      Optimal
                    </p>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <p className="text-3xl font-bold text-yellow-600">
                      {data.lab_analysis.biomarker_categories_summary.keep_in_mind_count || 0}
                    </p>
                    <p className="text-sm text-yellow-700 font-medium">
                      Keep in Mind
                    </p>
                  </div>
                  <div className="bg-red-50 p-4 rounded-lg">
                    <p className="text-3xl font-bold text-red-600">
                      {data.lab_analysis.biomarker_categories_summary.attention_needed_count || 0}
                    </p>
                    <p className="text-sm text-red-700 font-medium">
                      Needs Attention
                    </p>
                  </div>
                </div>
              )}

              {/* Detailed Biomarkers */}
              <div className="space-y-3">
                {(data.lab_analysis.detailed_biomarkers || []).map((biomarker, idx) => (
                  <div
                    key={idx}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">
                        {biomarker.biomarker_name}
                      </h4>
                      <span
                        className={`status-badge ${getStatusColor(
                          biomarker.status
                        )}`}
                      >
                        {biomarker.status.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                      <div>
                        <span className="text-gray-600">Your Value: </span>
                        <span className="font-medium text-gray-900">
                          {biomarker.value} {biomarker.unit}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600">Optimal Range: </span>
                        <span className="font-medium text-gray-900">
                          {biomarker.optimal_range}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">
                      {biomarker.interpretation}
                    </p>
                    {biomarker.recommendations && biomarker.recommendations.length > 0 && (
                      <ul className="text-sm text-gray-600 space-y-1">
                        {biomarker.recommendations.map((rec, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-primary-600 mt-0.5">→</span>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Four Pillars */}
      {data.four_pillars && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">
          <button
            onClick={() => toggleSection('pillars')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-gray-900">
              💪 Four Pillars Health Score
            </h3>
            {expandedSections.pillars ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>

          {expandedSections.pillars && (
            <div className="px-6 pb-6 grid md:grid-cols-2 gap-6">
              {Object.entries(data.four_pillars || {}).map(([key, pillar]) => (
                <div
                  key={key}
                  className="border border-gray-200 rounded-lg p-4"
                >
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-900 capitalize">
                      {key === 'eat' && '🍽️ '}
                      {key === 'sleep' && '😴 '}
                      {key === 'move' && '🏃 '}
                      {key === 'recover' && '🧘 '}
                      {key}
                    </h4>
                    <span
                      className={`text-2xl font-bold ${getPillarScoreColor(
                        pillar.score
                      )}`}
                    >
                      {pillar.score}/10
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mb-3">{pillar.summary}</p>
                  {pillar.action_items && pillar.action_items.length > 0 && (
                    <div className="space-y-1">
                      <p className="text-xs font-medium text-gray-600 uppercase">
                        Action Items:
                      </p>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {pillar.action_items.slice(0, 3).map((item, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-primary-600">✓</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Supplements */}
      {data.supplements && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">
          <button
            onClick={() => toggleSection('supplements')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-gray-900">
              💊 Supplement Recommendations (
              {data.supplements.recommended_supplements?.length || 0})
            </h3>
            {expandedSections.supplements ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>

          {expandedSections.supplements && (
            <div className="px-6 pb-6 space-y-4">
              {data.supplements.supplement_summary && (
                <p className="text-gray-700 bg-purple-50 p-4 rounded-lg">
                  {data.supplements.supplement_summary}
                </p>
              )}

              <div className="grid gap-4">
                {(data.supplements.recommended_supplements || []).map((supp, idx) => (
                  <div
                    key={idx}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">
                        {supp.supplement_name}
                      </h4>
                      <span
                        className={`status-badge ${getPriorityColor(
                          supp.priority
                        )}`}
                      >
                        {supp.priority} priority
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                      <div>
                        <span className="text-gray-600">Dosage: </span>
                        <span className="font-medium text-gray-900">
                          {supp.dosage}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600">Timing: </span>
                        <span className="font-medium text-gray-900">
                          {supp.timing}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">
                      <span className="font-medium">Reason: </span>
                      {supp.reason}
                    </p>
                    {supp.cautions && (
                      <p className="text-sm text-orange-700 bg-orange-50 p-2 rounded">
                        <span className="font-medium">⚠️ Caution: </span>
                        {supp.cautions}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Medical Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-sm text-yellow-900">
          <span className="font-semibold">⚠️ Medical Disclaimer:</span> This
          analysis is for informational and educational purposes only. Always
          consult with a qualified healthcare provider before making any
          decisions about your health or treatment.
        </p>
      </div>
    </div>
  );
}
