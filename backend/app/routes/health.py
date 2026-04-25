"""
Health Check Routes
Provides basic health check and status endpoints.
"""

from flask import Blueprint, jsonify
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        JSON: Status and version information
    """
    return jsonify({
        "status": "healthy",
        "service": "HealthAI Backend API",
        "version": "2.0.0",
        "environment": os.environ.get('FLASK_ENV', 'development')
    }), 200


@health_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint."""
    return jsonify({"message": "pong"}), 200
