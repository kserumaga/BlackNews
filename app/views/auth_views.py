from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.user_model import User
from app.utils.decorators import role_required  # Import the decorator
import jwt
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from app.services.access_control import update_user_role
from flask_login import current_user, login_user

auth_bp = Blueprint('auth', __name__)
db = SQLAlchemy()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        user = User.authenticate(email, password)
        if user:
            login_user(user, remember=True)
            flash('Login successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('auth/login.html')

def validate_jwt(token):
    # Use the validated secret key
    decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    # ... rest of validation logic

@auth_bp.route('/manage_access', methods=['GET', 'POST'])
@role_required('admin')  # Only allow admins to access this route
def manage_access():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash('User role updated successfully!', 'success')
    users = User.query.all()
    return render_template('manage_access.html', users=users)

@auth_bp.route('/logout')
def logout():
    # Logic to log out the user
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))