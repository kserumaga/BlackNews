from flask import Flask, render_template, current_app, request
from app.config import Config
from app.views.auth_views import auth_bp
from flask_login import LoginManager, current_user
from importlib import reload
from app.services.supabase import supabase
from flask_limiter import Limiter
from datetime import datetime

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    
    # Development-only: Auto-reload modules
    if app.config['DEBUG']:
        with app.app_context():
            from app import user_model
            reload(user_model)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    
    # Initialize Supabase
    supabase.init_app(app)

    # Import user model after app creation
    from app.user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route('/')
    def home():
        return render_template('index.html')  # or 'dashboard.html'

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=lambda: f"{request.remote_addr}-{current_user.id if current_user.is_authenticated else 'anon'}"
    )
    
    # Apply rate limits to auth routes
    limiter.limit("10/minute")(main_bp)

    # Add custom filters
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%b %d, %Y'):
        try:
            if isinstance(value, datetime):
                return value.strftime(format)
            
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(value).strftime(format)
            
            if isinstance(value, str):
                # Handle ISO format with timezone offset
                if 'Z' in value:
                    value = value.replace('Z', '+00:00')
                return datetime.fromisoformat(value).strftime(format)
            
            return "N/A"
        except Exception as e:
            app.logger.error(f"Datetimeformat error: {str(e)} Value: {value}")
            return "N/A"

    return app