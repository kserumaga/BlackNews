from flask import Flask
from app.config import Config
from app.views.auth_views import auth_bp  # Import the blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY  # Use validated secret
    app.config['DEBUG'] = Config.DEBUG  # Use centralized debug flag

    @app.route('/')
    def home():
        return "Welcome to BlackNews!"

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the blueprint

    return app