from supabase import create_client
from app.utils.security import hash_password, verify_password
from app.extensions import db
from app.config import Config  # Import Config to access SUPABASE_URL and SUPABASE_KEY

class User(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    google_id = db.Column(db.String)
    preferred_sources = db.Column(db.ARRAY(db.String))
    trust_score = db.Column(db.Float)
    admin_level = db.Column(db.Integer)
    user_level = db.Column(db.Integer)

    def __init__(self, email, password=None, google_id=None, preferred_sources=None, trust_score=0.5, admin_level=0, user_level=1):

        """
        Constructor for the User class.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to None.
            google_id (str, optional): The user's Google ID. Defaults to None.
            preferred_sources (list, optional): The user's preferred sources. Defaults to None.
            trust_score (float, optional): The user's trust score. Defaults to 0.5.
            admin_level (int, optional): The user's admin level. Defaults to 0.
            user_level (int, optional): The user's user level. Defaults to 1.
        """

        self.email = email
        self.password = hash_password(password) if password else None
        self.google_id = google_id
        self.preferred_sources = preferred_sources or []
        self.trust_score = trust_score
        self.admin_level = admin_level
        self.user_level = user_level

    def save(self):
        # Save user to Supabase
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        supabase.table('user_profile').insert({
            'email': self.email,
            'password': self.password,
            'google_id': self.google_id,
            'preferred_sources': self.preferred_sources,
            'trust_score': self.trust_score,
            'admin_level': self.admin_level,
            'user_level': self.user_level
        }).execute()

    def check_password(self, password):
        # Implement proper password hashing here
        return self.password == password