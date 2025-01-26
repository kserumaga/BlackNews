from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services.auth_service import authenticate_user
from app.utils.security import create_jwt_token
from app.config import Config
import jwt
from app.models.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        print(f"Queried user: {user}")
        if user:
            if user.check_password(data['password']):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, please try again.', 'danger')
        else:
            flash('User not found, please check your email.', 'danger')
    return render_template('login.html')

def validate_jwt(token):
    # Use the validated secret key
    decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    # ... rest of validation logic