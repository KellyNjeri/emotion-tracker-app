import os
import re

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hackathon-only'
    
    # Handle both SQLite and PostgreSQL URLs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False