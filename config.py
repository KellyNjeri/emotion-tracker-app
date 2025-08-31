import os
import re

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hackathon-only'
    
    # Get database URL from environment or use SQLite as default
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Handle PostgreSQL URL format
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Default to SQLite for development
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "health.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False