/**
 * API Client for HealthAI Backend
 * Handles all HTTP requests to the Flask backend
 */

import axios, { AxiosError, AxiosInstance } from 'axios';
import type { AnalysisResponse, MonthlyReportResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 300000, // 5 minutes for AI processing
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`[API] Response from ${response.config.url}:`, response.status);
        return response;
      },
      (error: AxiosError) => {
        console.error('[API] Response error:', error.message);
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: AxiosError): Error {
    if (error.response) {
      // Server responded with error status
      const message = (error.response.data as any)?.error || error.message;
      return new Error(`API Error: ${message}`);
    } else if (error.request) {
      // Request made but no response
      return new Error('No response from server. Please check your connection.');
    } else {
      // Error setting up request
      return new Error(`Request failed: ${error.message}`);
    }
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  /**
   * Analyze health data
   */
  async analyzeHealth(
    labReports: File[],
    healthAssessment?: File
  ): Promise<AnalysisResponse> {
    const formData = new FormData();

    // Add lab reports
    labReports.forEach((file) => {
      formData.append('lab_reports', file);
    });

    // Add health assessment if provided
    if (healthAssessment) {
      formData.append('health_assessment', healthAssessment);
    }

    // DON'T set Content-Type manually - let axios set it with the boundary
    const response = await this.client.post<AnalysisResponse>('/analyze', formData);

    return response.data;
  }

  /**
   * Generate monthly report
   */
  async generateMonthlyReport(
    previousLabReport: File,
    dailyLogs: File,
    weeklyAssessments?: File
  ): Promise<MonthlyReportResponse> {
    const formData = new FormData();

    formData.append('previous_lab_report', previousLabReport);
    formData.append('daily_logs', dailyLogs);

    if (weeklyAssessments) {
      formData.append('weekly_assessments', weeklyAssessments);
    }

    // DON'T set Content-Type manually - let axios set it with the boundary
    const response = await this.client.post<MonthlyReportResponse>('/monthly-report', formData);

    return response.data;
  }

  /**
   * Get analysis summary
   */
  async getAnalysisSummary(analysisData: any): Promise<any> {
    const response = await this.client.post('/analyze/summary', {
      analysis_data: analysisData,
    });
    return response.data;
  }

  /**
   * Get monthly report summary
   */
  async getMonthlyReportSummary(reportData: any): Promise<any> {
    const response = await this.client.post('/monthly-report/summary', {
      report_data: reportData,
    });
    return response.data;
  }

  /**
   * Send chat message (placeholder)
   */
  async sendChatMessage(message: string, context?: any): Promise<any> {
    const response = await this.client.post('/chat', {
      message,
      context,
    });
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export class for testing
export default APIClient;
