from app.models.user_model import User

def create_admin_user(email, password):
    # Logic to create an admin user
    print(f"Admin user created with email: {email}")

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        print(f"User found: {user.email}")
        if user.check_password(password):
            print("Password match")
            return user
        else:
            print("Password does not match")
    else:
        print("User not found")
    return None