"""
Analysis Service for HealthAI
Handles health analysis logic and AI processing.
"""

from typing import Dict, List, Optional
from app.utils import (
    HealthAIClient,
    build_biomarker_prompt,
    build_four_pillars_prompt,
    build_supplements_prompt,
    load_json_schema,
    validate_biomarker_count
)
from config.config import AIConfig


class AnalysisService:
    """Service for processing health analysis requests."""

    def __init__(self):
        """Initialize the analysis service with AI client."""
        self.ai_client = HealthAIClient(max_output_tokens=AIConfig.MAX_OUTPUT_TOKENS_STANDARD)

        # Load schemas
        self.schema_biomarkers = load_json_schema('biomarkers.json')
        self.schema_4pillars = load_json_schema('four_pillars.json')
        self.schema_supplements = load_json_schema('supplements.json')

    def analyze_health_data(
        self,
        lab_report_text: str,
        health_assessment_text: Optional[str] = None
    ) -> Dict:
        """
        Perform complete health analysis including biomarkers, four pillars, and supplements.

        Args:
            lab_report_text: Combined text from lab reports
            health_assessment_text: Optional health assessment text

        Returns:
            Dict: Complete analysis results containing all three parts

        Raises:
            Exception: If analysis fails
        """
        # Use placeholder if no health assessment provided
        if not health_assessment_text:
            health_assessment_text = "No additional health information provided. Analysis based on lab reports only."

        final_combined_output = {}
        analysis_status = []

        # Part 1: Biomarkers Analysis
        try:
            analysis_status.append({
                "step": "biomarkers",
                "status": "processing",
                "message": "Analyzing biomarkers..."
            })

            biomarker_prompt = build_biomarker_prompt(
                health_assessment_text,
                lab_report_text
            )

            biomarker_data_raw, _ = self.ai_client.generate_content(
                biomarker_prompt,
                self.schema_biomarkers
            )

            if biomarker_data_raw:
                final_combined_output.update(biomarker_data_raw)

            analysis_status.append({
                "step": "biomarkers",
                "status": "completed",
                "message": "Biomarker analysis complete"
            })

        except Exception as e:
            analysis_status.append({
                "step": "biomarkers",
                "status": "failed",
                "message": f"Failed to analyze biomarkers: {str(e)}"
            })
            raise

        # Part 2: Four Pillars Analysis
        try:
            analysis_status.append({
                "step": "four_pillars",
                "status": "processing",
                "message": "Analyzing Four Pillars (Eat, Sleep, Move, Recover)..."
            })

            four_pillars_prompt = build_four_pillars_prompt(
                health_assessment_text,
                lab_report_text
            )

            four_pillars_data_raw, _ = self.ai_client.generate_content(
                four_pillars_prompt,
                self.schema_4pillars
            )

            if four_pillars_data_raw:
                final_combined_output.update(four_pillars_data_raw)

            analysis_status.append({
                "step": "four_pillars",
                "status": "completed",
                "message": "Four Pillars analysis complete"
            })

        except Exception as e:
            analysis_status.append({
                "step": "four_pillars",
                "status": "failed",
                "message": f"Failed to analyze four pillars: {str(e)}"
            })
            raise

        # Part 3: Supplements Analysis
        try:
            analysis_status.append({
                "step": "supplements",
                "status": "processing",
                "message": "Creating supplement recommendations..."
            })

            supplements_prompt = build_supplements_prompt(
                health_assessment_text,
                lab_report_text
            )

            supplements_data_raw, _ = self.ai_client.generate_content(
                supplements_prompt,
                self.schema_supplements
            )

            if supplements_data_raw:
                final_combined_output.update(supplements_data_raw)

            analysis_status.append({
                "step": "supplements",
                "status": "completed",
                "message": "Supplements analysis complete"
            })

        except Exception as e:
            analysis_status.append({
                "step": "supplements",
                "status": "failed",
                "message": f"Failed to analyze supplements: {str(e)}"
            })
            raise

        # Post-processing: Validate and correct biomarker counts
        if "lab_analysis" in final_combined_output and final_combined_output["lab_analysis"]:
            final_combined_output["lab_analysis"] = validate_biomarker_count(
                final_combined_output["lab_analysis"]
            )

        return {
            "success": True,
            "data": final_combined_output,
            "status": analysis_status
        }

    def get_analysis_summary(self, analysis_data: Dict) -> Dict:
        """
        Generate a summary of the analysis results.

        Args:
            analysis_data: Complete analysis data

        Returns:
            Dict: Summary information
        """
        summary = {
            "biomarkers_tested": 0,
            "optimal_count": 0,
            "attention_needed_count": 0,
            "four_pillars_scores": {},
            "supplements_count": 0
        }

        # Extract biomarker summary
        if "lab_analysis" in analysis_data:
            lab_analysis = analysis_data["lab_analysis"]
            summary["biomarkers_tested"] = lab_analysis.get("biomarkers_tested_count", 0)

            if "biomarker_categories_summary" in lab_analysis:
                cat_summary = lab_analysis["biomarker_categories_summary"]
                summary["optimal_count"] = cat_summary.get("optimal_count", 0)
                summary["attention_needed_count"] = cat_summary.get("attention_needed_count", 0)

        # Extract four pillars scores
        if "four_pillars" in analysis_data:
            pillars = analysis_data["four_pillars"]
            summary["four_pillars_scores"] = {
                "eat": pillars.get("eat", {}).get("score", 0),
                "sleep": pillars.get("sleep", {}).get("score", 0),
                "move": pillars.get("move", {}).get("score", 0),
                "recover": pillars.get("recover", {}).get("score", 0)
            }

        # Extract supplements count
        if "supplements" in analysis_data:
            supplements = analysis_data["supplements"]
            summary["supplements_count"] = len(supplements.get("recommended_supplements", []))

        return summary
