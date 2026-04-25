"""
HealthAI Backend Application Entry Point

Run this file to start the Flask development server.
For production, use gunicorn with the create_app factory.

Usage:
    Development: python run.py
    Production: gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
"""

import os
from app import create_app

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create application instance
app = create_app(config_name)

if __name__ == '__main__':
    # Development server configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║        🌿 HealthAI Backend API Server v2.0.0         ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝

    Server running at: http://{host}:{port}
    Environment: {config_name}
    Debug mode: {debug}

    API Endpoints:
    ✓ Health Check:       GET  /api/health
    ✓ Ping:               GET  /api/ping
    ✓ Analyze Health:     POST /api/analyze
    ✓ Monthly Report:     POST /api/monthly-report
    ✓ Chat:               POST /api/chat

    Press CTRL+C to quit
    """)

    app.run(
        host=host,
        port=port,
        debug=debug
    )
