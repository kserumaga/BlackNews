from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

class Config:
    # Supabase Only
    SUPABASE_URL = os.getenv('SUPABASE_URL')  # Should look like https://[id].supabase.co
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')  # Anon/public key from Supabase
    
    # Flask-Login
    SECRET_KEY = os.getenv('SECRET_KEY')  # Required for sessions
    
    # Debug should default to False in production
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Add session protection
    SESSION_COOKIE_SECURE = True  # Requires HTTPS
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    @classmethod
    def validate(cls):
        """Check for minimum security requirements"""
        if not cls.SECRET_KEY or len(cls.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        if not cls.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is missing. Check your .env file")
        if not cls.SUPABASE_URL.startswith('https://') or '.supabase.co' not in cls.SUPABASE_URL:
            raise ValueError(f"Invalid SUPABASE_URL: {cls.SUPABASE_URL} - Must be https://[project-id].supabase.co")
        if not cls.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is missing. Check your .env file")
        if not cls.SUPABASE_KEY.startswith('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'):
            raise ValueError("Invalid SUPABASE_KEY - Get the anon/public key from Supabase")

# Validate configuration on import
Config.validate()

print("Loaded SUPABASE_URL:", Config.SUPABASE_URL)