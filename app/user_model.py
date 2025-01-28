from app.services.supabase import supabase
from flask_login import UserMixin
from flask import current_app
import bcrypt
from app.config import Config
import requests
from datetime import datetime

print("User class reloaded!")  # Add temporary line

class User(UserMixin):
    def __init__(self, id, email, created_at=None, is_admin=False):
        self.id = id
        self.email = email
        self.created_at = created_at or datetime.now()
        self.is_admin = is_admin

    @classmethod
    def authenticate(cls, email, password):
        """Official client auth method"""
        try:
            # Direct authentication without admin API
            response = supabase.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Verify we actually got a session
            if not response.session:
                current_app.logger.error("No session in auth response")
                return None
            
            return cls(
                id=response.user.id,
                email=response.user.email,
                created_at=datetime.fromisoformat(response.user.created_at),
                is_admin=response.user.user_metadata.get('is_admin', False)
            )
        
        except Exception as e:
            current_app.logger.error(f"Auth error: {str(e)}")
            return None

    @classmethod
    def get(cls, user_id):
        """Get user from auth response"""
        try:
            # Get current session instead of admin API
            session = supabase.client.auth.get_session()
            if session.user.id == user_id:
                return cls(
                    id=session.user.id,
                    email=session.user.email,
                    is_admin=session.user.user_metadata.get('is_admin', False)
                )
            return None
        except Exception as e:
            current_app.logger.error(f"User fetch error: {str(e)}")
            return None 