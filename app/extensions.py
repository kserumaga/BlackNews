from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SUPABASE_URL
    db.init_app(app)
