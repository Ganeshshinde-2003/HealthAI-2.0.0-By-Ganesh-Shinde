/**
 * TypeScript type definitions for HealthAI Frontend
 */

// Analysis Types
export interface BiomarkerData {
  biomarker_name: string;
  value: string;
  unit: string;
  reference_range: string;
  optimal_range: string;
  status: 'optimal' | 'keep_in_mind' | 'attention_needed';
  interpretation: string;
  recommendations?: string[];
}

export interface LabAnalysis {
  biomarkers_tested_count?: number;
  detailed_biomarkers?: BiomarkerData[];
  biomarker_categories_summary?: {
    optimal_count?: number;
    keep_in_mind_count?: number;
    attention_needed_count?: number;
    description_text?: string;
  };
}

export interface PillarScore {
  score: number;
  status: string;
  summary: string;
  recommendations?: string[];
  action_items?: string[];
}

export interface FourPillars {
  eat: PillarScore;
  sleep: PillarScore;
  move: PillarScore;
  recover: PillarScore;
}

export interface Supplement {
  supplement_name: string;
  dosage: string;
  timing: string;
  reason: string;
  priority: 'high' | 'medium' | 'low';
  cautions: string;
}

export interface SupplementsData {
  recommended_supplements?: Supplement[];
  supplement_summary?: string;
}

export interface AnalysisResult {
  lab_analysis?: LabAnalysis;
  four_pillars?: FourPillars;
  supplements?: SupplementsData;
}

export interface AnalysisResponse {
  success: boolean;
  data?: AnalysisResult;
  status?: Array<{
    step: string;
    status: string;
    message: string;
  }>;
  error?: string;
}

// Monthly Report Types
export interface MonthlyReportData {
  month_summary: {
    month: string;
    overall_trend: string;
    key_improvements: string[];
    key_concerns: string[];
  };
  hormonal_insights?: any;
  daily_log_patterns?: any;
  radar_chart_data?: any;
}

export interface MonthlyReportResponse {
  success: boolean;
  data?: MonthlyReportData;
  message?: string;
  error?: string;
}

// UI State Types
export interface UploadedFile {
  file: File;
  preview?: string;
  error?: string;
}

export interface AnalysisState {
  isAnalyzing: boolean;
  progress: number;
  currentStep: string;
  error?: string;
  result?: AnalysisResult;
}
