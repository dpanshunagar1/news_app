#!/usr/bin/env python3
"""
Flask Application Entry Point

This script starts the Flask development server.

Usage:
    python run.py
"""

from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    print("Starting News Aggregator...")
    print("Visit http://127.0.0.1:5000 to view the application")
    print("API endpoint available at: http://127.0.0.1:5000/api/articles")
    
    # Run Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)
