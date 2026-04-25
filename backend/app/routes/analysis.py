"""
Health Analysis Routes
Handles standard health analysis requests.
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.services import AnalysisService
from app.utils import extract_text_from_file, FileProcessingError, transform_analysis_response

analysis_bp = Blueprint('analysis', __name__)
analysis_service = AnalysisService()


@analysis_bp.route('/analyze', methods=['POST'])
def analyze_health():
    """
    Perform health analysis on uploaded files.

    Expected form data:
        - lab_reports: One or more lab report files (required)
        - health_assessment: Health assessment file (optional)

    Returns:
        JSON: Analysis results or error message
    """
    try:
        # Check if lab reports are provided
        if 'lab_reports' not in request.files:
            return jsonify({
                "success": False,
                "error": "No lab report files provided"
            }), 400

        lab_report_files = request.files.getlist('lab_reports')

        if not lab_report_files or all(f.filename == '' for f in lab_report_files):
            return jsonify({
                "success": False,
                "error": "No lab report files selected"
            }), 400

        # Process lab reports
        raw_lab_report_inputs = []
        for file in lab_report_files:
            if file and file.filename:
                try:
                    extracted_text = extract_text_from_file(file)
                    raw_lab_report_inputs.append(
                        f"--- Start Lab Report: {file.filename} ---\n{extracted_text}\n--- End Lab Report: {file.filename} ---"
                    )
                except FileProcessingError as e:
                    return jsonify({
                        "success": False,
                        "error": f"Error processing file '{file.filename}': {str(e)}"
                    }), 400

        combined_lab_report_text = "\n\n".join(raw_lab_report_inputs)

        # Format lab report section
        lab_report_section_formatted = f"""
Here is the user's Lab Report text (potentially multiple reports combined):
{combined_lab_report_text}
"""

        # Process health assessment (optional)
        raw_health_assessment_input = ""
        if 'health_assessment' in request.files:
            health_file = request.files['health_assessment']
            if health_file and health_file.filename:
                try:
                    raw_health_assessment_input = extract_text_from_file(health_file)
                except FileProcessingError as e:
                    # Continue with analysis even if health assessment fails
                    print(f"Warning: Error processing health assessment: {e}")

        # Perform analysis
        result = analysis_service.analyze_health_data(
            lab_report_text=lab_report_section_formatted,
            health_assessment_text=raw_health_assessment_input if raw_health_assessment_input else None
        )

        # Transform response to match frontend expected format
        transformed_result = transform_analysis_response(result)

        return jsonify(transformed_result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500


@analysis_bp.route('/analyze/summary', methods=['POST'])
def get_analysis_summary():
    """
    Get a summary of analysis data.

    Expected JSON body:
        - analysis_data: Complete analysis results

    Returns:
        JSON: Summary of the analysis
    """
    try:
        data = request.get_json()

        if not data or 'analysis_data' not in data:
            return jsonify({
                "success": False,
                "error": "No analysis data provided"
            }), 400

        summary = analysis_service.get_analysis_summary(data['analysis_data'])

        return jsonify({
            "success": True,
            "summary": summary
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to generate summary: {str(e)}"
        }), 500
