from flask import Blueprint, request, jsonify
from app.services.auth_service import authenticate_user
from app.utils.security import create_jwt_token
from app.config import Config
import jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if user:
        token = create_jwt_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

def validate_jwt(token):
    # Use the validated secret key
    decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    # ... rest of validation logic