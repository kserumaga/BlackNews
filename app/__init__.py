from flask import Flask, render_template
from app.config import Config
from app.views.auth_views import auth_bp
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SUPABASE_URL
    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('index.html')  # or 'dashboard.html'

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app