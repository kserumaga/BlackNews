from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Access other environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')  # Set to "True" to enable debug mode