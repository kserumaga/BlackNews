from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                flash('You do not have access to this page.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 