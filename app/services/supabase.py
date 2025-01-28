from supabase import create_client
from flask import current_app

class SupabaseClient:
    def __init__(self, app=None):
        self.client = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.client = create_client(
            app.config['SUPABASE_URL'],
            app.config['SUPABASE_KEY']  # Use anon key for client-side
        )
        # Service role for admin operations
        self.admin = create_client(
            app.config['SUPABASE_URL'],
            app.config['SUPABASE_KEY']
        )
    
    def __getattr__(self, name):
        if not self.client:
            raise RuntimeError("Supabase client not initialized")
        return getattr(self.client, name)

supabase = SupabaseClient()
