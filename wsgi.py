"""
WSGI entry point for production servers (gunicorn, etc.)
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app

# Create Flask application
app = create_app()

if __name__ == "__main__":
    app.run()
