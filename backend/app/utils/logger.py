"""
Logging utility for HealthAI Backend
Provides centralized logging configuration and request tracking.
"""

import logging
import os
from datetime import datetime
from flask import request, g


def setup_logging(app):
    """
    Configure logging for Flask application.

    Creates logs directory and sets up logging for both file and console output.
    """
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'backend_{datetime.now().strftime("%Y%m%d")}.log')

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Get logger for app
    logger = logging.getLogger('healthai')
    logger.setLevel(logging.INFO)

    return logger


def get_logger(name='healthai'):
    """Get a logger instance."""
    return logging.getLogger(name)


def setup_request_logging(app):
    """
    Set up request/response logging middleware.
    Logs details about each API request.
    """
    logger = get_logger()

    @app.before_request
    def log_request():
        """Log incoming API request."""
        g.start_time = datetime.now()

        # Extract relevant request info
        method = request.method
        path = request.path
        remote_addr = request.remote_addr
        user_agent = request.user_agent

        # Log request
        logger.info(f"→ REQUEST: {method} {path} from {remote_addr}")

        # Log file uploads
        if request.files:
            files_info = [f"{name}: {file.filename}" for name, file in request.files.items(multi=True)]
            logger.info(f"  Files: {', '.join(files_info)}")

        # Log JSON data (exclude sensitive info)
        if request.is_json and request.get_json():
            data = request.get_json()
            safe_data = {k: v for k, v in data.items() if k not in ['password', 'token', 'secret']}
            logger.info(f"  Data: {safe_data}")

    @app.after_request
    def log_response(response):
        """Log API response."""
        logger.info(f"← RESPONSE: {response.status_code} ({request.method} {request.path})")

        # Calculate request duration
        if hasattr(g, 'start_time'):
            duration = (datetime.now() - g.start_time).total_seconds()
            logger.info(f"  Duration: {duration:.3f}s")

        return response


def log_error(error_msg, exception=None):
    """Log an error with optional exception details."""
    logger = get_logger()
    if exception:
        logger.error(f"ERROR: {error_msg}", exc_info=True)
    else:
        logger.error(f"ERROR: {error_msg}")


def log_info(message):
    """Log an info message."""
    logger = get_logger()
    logger.info(message)


def log_warning(message):
    """Log a warning message."""
    logger = get_logger()
    logger.warning(message)
