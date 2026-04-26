"""
Monthly Report Routes
Handles monthly health report generation requests.
"""

from flask import Blueprint, request, jsonify
from app.services import MonthlyReportService
from app.utils import extract_text_from_file, FileProcessingError
from app.utils.logger import get_logger, log_error

monthly_bp = Blueprint('monthly', __name__)
monthly_service = MonthlyReportService()
logger = get_logger()


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
    logger.info("📅 /monthly-report endpoint called - generating monthly report")
    try:
        # Check required files
        if 'previous_lab_report' not in request.files:
            logger.warning("  ⚠ Previous lab report file is missing")
            return jsonify({
                "success": False,
                "error": "Previous lab report file is required"
            }), 400

        if 'daily_logs' not in request.files:
            logger.warning("  ⚠ Daily logs file is missing")
            return jsonify({
                "success": False,
                "error": "Daily logs file is required"
            }), 400

        # Process previous lab report
        lab_file = request.files['previous_lab_report']
        if not lab_file or lab_file.filename == '':
            logger.warning("  ⚠ Lab report file not selected")
            return jsonify({
                "success": False,
                "error": "No lab report file selected"
            }), 400

        try:
            logger.info(f"  📄 Extracting previous lab report: {lab_file.filename}")
            previous_lab_report_text = extract_text_from_file(lab_file)
            logger.info(f"    ✓ Lab report processed ({len(previous_lab_report_text)} chars)")
        except FileProcessingError as e:
            logger.error(f"    ✗ Error processing lab report: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"Error processing lab report: {str(e)}"
            }), 400

        # Process daily logs
        logs_file = request.files['daily_logs']
        if not logs_file or logs_file.filename == '':
            logger.warning("  ⚠ Daily logs file not selected")
            return jsonify({
                "success": False,
                "error": "No daily logs file selected"
            }), 400

        try:
            logger.info(f"  📝 Extracting daily logs: {logs_file.filename}")
            daily_logs_text = extract_text_from_file(logs_file)
            logger.info(f"    ✓ Daily logs processed ({len(daily_logs_text)} chars)")
        except FileProcessingError as e:
            logger.error(f"    ✗ Error processing daily logs: {str(e)}")
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
                    logger.info(f"  📊 Extracting weekly assessments: {weekly_file.filename}")
                    weekly_assessments_text = extract_text_from_file(weekly_file)
                    logger.info(f"    ✓ Weekly assessments processed")
                except FileProcessingError as e:
                    logger.warning(f"    ⚠ Error processing weekly assessments: {e}")

        # Generate report
        logger.info("  🤖 Running monthly report generation service...")
        result = monthly_service.generate_monthly_report(
            previous_lab_report_text=previous_lab_report_text,
            daily_logs_text=daily_logs_text,
            weekly_assessments_text=weekly_assessments_text
        )

        logger.info("✓ Monthly report generated successfully")
        return jsonify(result), 200

    except Exception as e:
        log_error(f"Monthly report generation failed: {str(e)}", e)
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
    logger.info("📊 /monthly-report/summary endpoint called - generating summary")
    try:
        data = request.get_json()

        if not data or 'report_data' not in data:
            logger.warning("  ⚠ No report data provided")
            return jsonify({
                "success": False,
                "error": "No report data provided"
            }), 400

        logger.info("  🔄 Generating monthly report summary...")
        summary = monthly_service.get_report_summary(data['report_data'])

        logger.info("✓ Monthly summary generated successfully")
        return jsonify({
            "success": True,
            "summary": summary
        }), 200

    except Exception as e:
        log_error(f"Failed to generate summary: {str(e)}", e)
        return jsonify({
            "success": False,
            "error": f"Failed to generate summary: {str(e)}"
        }), 500
