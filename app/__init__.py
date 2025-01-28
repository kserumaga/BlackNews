from flask import Flask, render_template
from app.config import Config
from app.views.auth_views import auth_bp
from flask_login import LoginManager
from importlib import reload
from app.services.supabase import supabase
from flask_limiter import Limiter
from datetime import datetime

login_manager = LoginManager()

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
    login_manager.login_view = 'auth.login'
    
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

    limiter = Limiter(key_func=lambda: current_user.id)
    limiter.init_app(app)

    # Add custom filters
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%b %d, %Y'):
        if isinstance(value, datetime):
            return value.strftime(format)
        try:
            return datetime.fromisoformat(value).strftime(format)
        except (TypeError, ValueError):
            return "N/A"

    return app