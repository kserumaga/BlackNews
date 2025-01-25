from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.utils.security import hash_password

class User:
    def __init__(self, email, password=None, google_id=None, preferred_sources=None, trust_score=0.5):

        """
        Constructor for the User class.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to None.
            google_id (str, optional): The user's Google ID. Defaults to None.
            preferred_sources (list, optional): The user's preferred sources. Defaults to None.
            trust_score (float, optional): The user's trust score. Defaults to 0.5.
        """

        self.email = email
        self.password = hash_password(password) if password else None
        self.google_id = google_id
        self.preferred_sources = preferred_sources or []
        self.trust_score = trust_score

    def save(self):
        # Save user to Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.table('users').insert({
            'email': self.email,
            'password': self.password,
            'google_id': self.google_id,
            'preferred_sources': self.preferred_sources,
            'trust_score': self.trust_score
        }).execute()