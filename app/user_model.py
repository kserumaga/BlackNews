from supabase import create_client
from flask_login import UserMixin
from flask import current_app
import bcrypt

print("User class reloaded!")  # Add temporary line

class User(UserMixin):
    def __init__(self, id, email, is_admin=False):
        self.id = id
        self.email = email
        self.is_admin = is_admin

    @classmethod
    def authenticate(cls, email, password):
        """Authenticate using Supabase's built-in auth"""
        supabase = create_client(
            current_app.config['SUPABASE_URL'],
            current_app.config['SUPABASE_KEY']
        )
        try:
            # Let Supabase handle password verification
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return cls.get(response.user.id)
        except Exception as e:
            current_app.logger.error(f"Auth error: {str(e)}")
            return None

    @classmethod
    def get(cls, user_id):
        """Retrieve user from Supabase"""
        supabase = create_client(
            current_app.config['SUPABASE_URL'],
            current_app.config['SUPABASE_KEY']
        )
        try:
            data = supabase.table('users', schema='auth').select('*').eq('id', user_id).execute()
            if data.data:
                user_data = data.data[0]
                return cls(
                    id=user_data['id'],
                    email=user_data['email'],
                    is_admin=user_data.get('raw_user_meta_data', {}).get('is_admin', False)
                )
            return None
        except Exception as e:
            current_app.logger.error(f"User lookup error: {str(e)}")
            return None 