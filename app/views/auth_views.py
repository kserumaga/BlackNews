from flask import request, jsonify
from app.services.auth_service import authenticate_user
from app.utils.security import create_jwt_token

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if user:
        token = create_jwt_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401