from supabase import create_client

from app.config import SUPABASE_KEY, SUPABASE_URL

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
