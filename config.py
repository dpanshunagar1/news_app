import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False
