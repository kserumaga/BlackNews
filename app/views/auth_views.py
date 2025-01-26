from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services.auth_service import authenticate_user
from app.utils.security import create_jwt_token
from app.config import Config
import jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = authenticate_user(data['email'], data['password'])
        if user:
            token = create_jwt_token(user.id)
            # Set token in session or cookie
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home or dashboard
        flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')  # Render login form

def validate_jwt(token):
    # Use the validated secret key
    decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    # ... rest of validation logic