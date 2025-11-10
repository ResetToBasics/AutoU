#!/bin/bash
# Start script for production deployment

# Use PORT from environment, default to 5000 if not set
PORT=${PORT:-5000}

# Start gunicorn
exec gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
