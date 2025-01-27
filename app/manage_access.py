from app.user_model import User
from app.extensions import db

def update_user_role(user_id, new_role):
    user = User.query.get(user_id)
    if user:
        user.role = new_role
        db.session.commit()
        return True
    return False 