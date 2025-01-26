# BLACKNEWS/app/utils/security.py
import pandas as pd
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.config import Config


def get_or_create_category(supabase, category_name):
    if pd.isna(category_name):
        return None
    response = supabase.table('categories').select('id').eq('name', category_name).execute()
    if response.data:
        return response.data[0]['id']
    else:
        new_category = supabase.table('categories').insert({"name": category_name}).execute()
        return new_category.data[0]['id']

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')