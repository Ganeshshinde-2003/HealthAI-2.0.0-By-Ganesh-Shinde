"""
API Routes for HealthAI Backend.
"""

from .health import health_bp
from .analysis import analysis_bp
from .monthly import monthly_bp
from .chat import chat_bp

__all__ = [
    'health_bp',
    'analysis_bp',
    'monthly_bp',
    'chat_bp'
]
