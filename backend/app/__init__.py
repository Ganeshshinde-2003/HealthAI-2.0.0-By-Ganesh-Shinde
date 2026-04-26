"""
HealthAI Flask Backend Application
Provides REST API for health analysis and monthly reports.

Version: 2.0.0
Author: Ganesh Shinde
"""

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app(config_name='development'):
    """
    Application factory for creating Flask app instances.

    Args:
        config_name: Configuration environment (development, production, testing)

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    from config.config import config
    app.config.from_object(config[config_name])

    # Initialize extensions
    from app.extensions import db
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from app.models import User, Analysis, MonthlyReport, ChatMessage, DailyLog

    # Enable CORS for Next.js frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:3001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes.health import health_bp
    from app.routes.analysis import analysis_bp
    from app.routes.monthly import monthly_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(monthly_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')

    return app
