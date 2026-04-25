"""
Monthly Report Service for HealthAI
Handles monthly health report generation logic.
"""

from typing import Dict, Optional
from app.utils import (
    HealthAIClient,
    build_monthly_report_prompt,
    load_json_schema
)
from config.config import AIConfig


class MonthlyReportService:
    """Service for processing monthly health report requests."""

    def __init__(self):
        """Initialize the monthly report service with AI client."""
        self.ai_client = HealthAIClient(max_output_tokens=AIConfig.MAX_OUTPUT_TOKENS_MONTHLY)
        self.schema_monthly = load_json_schema('monthly_report.json')

    def generate_monthly_report(
        self,
        previous_lab_report_text: str,
        daily_logs_text: str,
        weekly_assessments_text: Optional[str] = None
    ) -> Dict:
        """
        Generate a comprehensive monthly health report.

        Args:
            previous_lab_report_text: Text from previous lab reports
            daily_logs_text: Text from daily health logs
            weekly_assessments_text: Optional weekly assessment text

        Returns:
            Dict: Monthly report data

        Raises:
            Exception: If report generation fails
        """
        # Use placeholder if no weekly assessments provided
        if not weekly_assessments_text:
            weekly_assessments_text = "No weekly assessments provided."

        try:
            # Build prompt
            monthly_prompt = build_monthly_report_prompt(
                previous_lab_report_text,
                daily_logs_text,
                weekly_assessments_text
            )

            # Generate report
            monthly_data, _ = self.ai_client.generate_content(
                monthly_prompt,
                self.schema_monthly
            )

            return {
                "success": True,
                "data": monthly_data,
                "message": "Monthly report generated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Failed to generate monthly report: {str(e)}"
            }

    def get_report_summary(self, report_data: Dict) -> Dict:
        """
        Generate a summary of the monthly report.

        Args:
            report_data: Complete monthly report data

        Returns:
            Dict: Summary information
        """
        summary = {
            "month": report_data.get("month_summary", {}).get("month", "Unknown"),
            "overall_trend": report_data.get("month_summary", {}).get("overall_trend", "Unknown"),
            "key_improvements": [],
            "key_concerns": []
        }

        # Extract key improvements and concerns
        if "month_summary" in report_data:
            month_summary = report_data["month_summary"]
            summary["key_improvements"] = month_summary.get("key_improvements", [])[:3]
            summary["key_concerns"] = month_summary.get("key_concerns", [])[:3]

        return summary
