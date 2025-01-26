from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

class Config:
    # Required security settings
    SUPABASE_URL = os.environ['SUPABASE_URL']  # Will raise error if missing
    SUPABASE_KEY = os.environ['SUPABASE_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    
    # Debug should default to False in production
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Check for minimum security requirements"""
        if len(cls.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        if not cls.SUPABASE_URL.startswith(('https://', 'postgresql://')):
            raise ValueError("Invalid Supabase URL format")

# Validate configuration on import
Config.validate()