import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # RSS Feed settings
    RSS_FEEDS = os.getenv('RSS_FEEDS', '').split(',')
    if not RSS_FEEDS or RSS_FEEDS == ['']:
        raise ValueError("RSS_FEEDS environment variable is required")
    
    # Pagination settings
    ARTICLES_PER_PAGE = 10
