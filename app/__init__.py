from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import Config

# Initialize SQLAlchemy components
Base = declarative_base()
engine = None
SessionLocal = None

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app

def init_db(app):
    """Initialize database connection and create tables"""
    global engine, SessionLocal
    
    engine = create_engine(app.config['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    
    # Import models to ensure they're registered with Base
    from app.models import Article
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def get_db_session():
    """Get a database session"""
    return SessionLocal()
