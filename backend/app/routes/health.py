"""
Health Check Routes
Provides basic health check and status endpoints.
"""

from flask import Blueprint, jsonify
import os
from app.extensions import db
from sqlalchemy import text

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


@health_bp.route('/warmup', methods=['GET'])
def warmup():
    """
    Warm-up endpoint to wake up backend and database.
    Called by frontend on page load to eliminate cold starts.

    This endpoint:
    - Wakes up the backend server (Render)
    - Wakes up the database (Neon)
    - Returns quickly with minimal data

    Returns:
        JSON: Status and ready state
    """
    db_status = "ready"

    try:
        # Simple database query to wake up Neon
        # Just count users (very fast query)
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
        db_status = "connected"
    except Exception as e:
        # Database not set up or connection issue
        # Still return success - backend is warm
        db_status = "not_connected"
        print(f"Warmup DB check failed (this is OK): {e}")

    return jsonify({
        "status": "warm",
        "backend": "ready",
        "database": db_status,
        "message": "Services are warming up"
    }), 200
