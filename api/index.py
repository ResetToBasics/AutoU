"""
Vercel serverless handler
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

# Create Flask app
app = create_app()

# Vercel expects the app to be named 'app'
# This is the WSGI application that Vercel will use
