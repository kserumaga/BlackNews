from supabase import create_client
from app.config import Config

client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)