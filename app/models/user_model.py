from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.utils.security import hash_password

class User:
    def __init__(self, email, password=None, google_id=None):

        """
        Constructor for the User class.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to None.
            google_id (str, optional): The user's Google ID. Defaults to None.
        """


        self.email = email
        self.password = hash_password(password) if password else None
        self.google_id = google_id

    def save(self):
        # Save user to Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.table('users').insert({
            'email': self.email,
            'password': self.password,
            'google_id': self.google_id
        }).execute()