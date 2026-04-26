"""
Configuration file for HealthAI Flask Backend.
Centralizes all configuration constants and settings.
"""

import os
from datetime import timedelta


# ==========================================
# Base Configuration
# ==========================================

class Config:
    """Base configuration class."""

    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'xls', 'txt', 'csv'}

    # Google Cloud Configuration (matching secrets.toml format)
    GCP_PROJECT_ID = os.environ.get('PROJECT_ID') or os.environ.get('GCP_PROJECT_ID')
    GCP_LOCATION = os.environ.get('LOCATION') or os.environ.get('GCP_LOCATION', 'us-central1')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_CREDENTIALS_JSON = os.environ.get('GOOGLE_CREDENTIALS_JSON')

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-secret-change-in-production'
    JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY') or 'jwt-refresh-dev-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Auth Configuration
    MAX_LOGIN_ATTEMPTS = 10
    ACCOUNT_LOCKOUT_MINUTES = 30
    EMAIL_VERIFICATION_EXPIRES_HOURS = 24

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_DEFAULT = '200 per hour'

    # Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@novahealth.com')

    # Frontend URL (for email links)
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    ENV = 'production'

    # Production-specific settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True


# ==========================================
# AI Model Configuration
# ==========================================

class AIConfig:
    """Configuration for HealthAI and Gemini model."""

    # Model Selection
    MODEL_NAME = "gemini-2.5-flash-lite"

    # Generation Configuration
    TEMPERATURE = 0.2  # Low for deterministic JSON output
    TOP_P = 0.95
    TOP_K = 64
    MAX_OUTPUT_TOKENS_STANDARD = 65535  # For standard analysis
    MAX_OUTPUT_TOKENS_MONTHLY = 8192    # For monthly reports
    RESPONSE_MIME_TYPE = "application/json"

    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2
    INITIAL_RETRY_DELAY = 1


# ==========================================
# File Processing Configuration
# ==========================================

class FileConfig:
    """Configuration for file upload and processing."""

    # Supported File Types
    SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]

    # File Size Limits (in bytes)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Text Extraction Settings
    TEXT_ENCODING = "utf-8"
    ENCODING_ERROR_HANDLING = "ignore"


# ==========================================
# Safety Settings
# ==========================================

class SafetyConfig:
    """Safety settings for AI model harm categories."""

    HARASSMENT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    HATE_SPEECH_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    SEXUALLY_EXPLICIT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    DANGEROUS_CONTENT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"


# ==========================================
# Validation Configuration
# ==========================================

class ValidationConfig:
    """Configuration for JSON validation."""

    # Schema validation settings
    VALIDATE_SCHEMAS = True
    STRICT_VALIDATION = True

    # Error messages
    EMPTY_RESPONSE_ERROR = "Model returned an empty response."
    JSON_DECODE_ERROR = "Failed to get valid JSON after {max_retries} attempts"
    VALIDATION_ERROR = "JSON validation failed"


# ==========================================
# Configuration Dictionary
# ==========================================

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


# ==========================================
# Export All Configs
# ==========================================

__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'TestingConfig',
    'AIConfig',
    'FileConfig',
    'SafetyConfig',
    'ValidationConfig',
    'config'
]
