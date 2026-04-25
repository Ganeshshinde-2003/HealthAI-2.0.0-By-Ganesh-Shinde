"""
Monthly Report Routes
Handles monthly health report generation requests.
"""

from flask import Blueprint, request, jsonify
from app.services import MonthlyReportService
from app.utils import extract_text_from_file, FileProcessingError

monthly_bp = Blueprint('monthly', __name__)
monthly_service = MonthlyReportService()


@monthly_bp.route('/monthly-report', methods=['POST'])
def generate_monthly_report():
    """
    Generate a monthly health report.

    Expected form data:
        - previous_lab_report: Previous lab report file (required)
        - daily_logs: Daily health logs file (required)
        - weekly_assessments: Weekly assessment file (optional)

    Returns:
        JSON: Monthly report data or error message
    """
    try:
        # Check required files
        if 'previous_lab_report' not in request.files:
            return jsonify({
                "success": False,
                "error": "Previous lab report file is required"
            }), 400

        if 'daily_logs' not in request.files:
            return jsonify({
                "success": False,
                "error": "Daily logs file is required"
            }), 400

        # Process previous lab report
        lab_file = request.files['previous_lab_report']
        if not lab_file or lab_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No lab report file selected"
            }), 400

        try:
            previous_lab_report_text = extract_text_from_file(lab_file)
        except FileProcessingError as e:
            return jsonify({
                "success": False,
                "error": f"Error processing lab report: {str(e)}"
            }), 400

        # Process daily logs
        logs_file = request.files['daily_logs']
        if not logs_file or logs_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No daily logs file selected"
            }), 400

        try:
            daily_logs_text = extract_text_from_file(logs_file)
        except FileProcessingError as e:
            return jsonify({
                "success": False,
                "error": f"Error processing daily logs: {str(e)}"
            }), 400

        # Process weekly assessments (optional)
        weekly_assessments_text = None
        if 'weekly_assessments' in request.files:
            weekly_file = request.files['weekly_assessments']
            if weekly_file and weekly_file.filename:
                try:
                    weekly_assessments_text = extract_text_from_file(weekly_file)
                except FileProcessingError as e:
                    print(f"Warning: Error processing weekly assessments: {e}")

        # Generate report
        result = monthly_service.generate_monthly_report(
            previous_lab_report_text=previous_lab_report_text,
            daily_logs_text=daily_logs_text,
            weekly_assessments_text=weekly_assessments_text
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Monthly report generation failed: {str(e)}"
        }), 500


@monthly_bp.route('/monthly-report/summary', methods=['POST'])
def get_monthly_summary():
    """
    Get a summary of monthly report data.

    Expected JSON body:
        - report_data: Complete monthly report results

    Returns:
        JSON: Summary of the monthly report
    """
    try:
        data = request.get_json()

        if not data or 'report_data' not in data:
            return jsonify({
                "success": False,
                "error": "No report data provided"
            }), 400

        summary = monthly_service.get_report_summary(data['report_data'])

        return jsonify({
            "success": True,
            "summary": summary
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to generate summary: {str(e)}"
        }), 500
