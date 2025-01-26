from app.models.user_model import User
from app.utils.security import verify_password

def create_admin_user(email, password):
    # Logic to create an admin user
    print(f"Admin user created with email: {email}")

def authenticate_user(email, password):
    # Logic to authenticate user
    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        return user
    return None