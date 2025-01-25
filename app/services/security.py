import bcrypt
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY
from cryptography.fernet import Fernet

# Generate a key for encryption
# In practice, store this securely and load it from an environment variable
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None

def encrypt_data(data):
    """Encrypt sensitive data."""
    return cipher.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data):
    """Decrypt sensitive data."""
    return cipher.decrypt(encrypted_data).decode('utf-8')