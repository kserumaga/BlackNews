from supabase import create_client
from app.extensions import db
from app.config import Config
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}  # Specify the schema
    id = db.Column(db.String, primary_key=True)  # UUID as string
    email = db.Column(db.String, nullable=False, unique=True)
    encrypted_password = db.Column(db.String)  # Match the column name
    role = db.Column(db.String)  # Add role field

    def __init__(self, email, password=None):
        self.email = email
        self.encrypted_password = self.hash_password(password) if password else None

    def save(self):
        # Save user to Supabase
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        supabase.table('users').insert({
            'email': self.email,
            'encrypted_password': self.encrypted_password
        }).execute()

    def check_password(self, password):
        if self.encrypted_password is None:
            return False
        # Convert the stored password to bytes
        return bcrypt.checkpw(password.encode('utf-8'), self.encrypted_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())