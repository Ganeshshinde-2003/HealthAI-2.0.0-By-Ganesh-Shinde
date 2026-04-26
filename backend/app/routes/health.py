"""
Health Check Routes
Provides basic health check and status endpoints.
"""

from flask import Blueprint, jsonify
import os
from app.extensions import db
from sqlalchemy import text
from app.utils.logger import get_logger

health_bp = Blueprint('health', __name__)
logger = get_logger()


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        JSON: Status and version information
    """
    logger.info("🏥 /health endpoint called - checking service status")
    result = {
        "status": "healthy",
        "service": "HealthAI Backend API",
        "version": "2.0.0",
        "environment": os.environ.get('FLASK_ENV', 'development')
    }
    logger.info(f"✓ Health check passed: {result['status']}")
    return jsonify(result), 200


@health_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint."""
    logger.info("🔔 /ping endpoint called")
    logger.info("✓ Pong response sent")
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
    logger.info("🔥 /warmup endpoint called - warming up services")
    db_status = "ready"

    try:
        logger.info("  📊 Testing database connection...")
        # Simple database query to wake up Neon
        # Just count users (very fast query)
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
        db_status = "connected"
        logger.info(f"  ✓ Database connected - {user_count} users found")
    except Exception as e:
        # Database not set up or connection issue
        # Still return success - backend is warm
        db_status = "not_connected"
        logger.warning(f"  ⚠ Warmup DB check failed (this is OK): {e}")

    result = {
        "status": "warm",
        "backend": "ready",
        "database": db_status,
        "message": "Services are warming up"
    }
    logger.info(f"✓ Warmup complete: backend={result['backend']}, db={db_status}")
    return jsonify(result), 200
