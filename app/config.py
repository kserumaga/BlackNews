from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # Ensure SUPABASE_URL is a valid SQLAlchemy database URL
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Debug should default to False in production
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Check for minimum security requirements"""
        if not cls.SECRET_KEY or len(cls.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        if not cls.SUPABASE_URL.startswith('postgresql://'):
            raise ValueError("SUPABASE_URL must be a valid PostgreSQL URL")

# Validate configuration on import
Config.validate()

print("Loaded SUPABASE_URL:", Config.SUPABASE_URL)