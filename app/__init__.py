# app/__init__.py
import os
from flask import Flask, session
from dotenv import load_dotenv
from .models.models import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # --- Daftarkan Blueprints ---
    from .auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .learning.routes import learning as learning_blueprint
    app.register_blueprint(learning_blueprint)

    @app.context_processor
    def inject_user():
        """Menyuntikkan data user ke semua template."""
        if 'username' in session:
            return {'current_user_name': session['username']}
        return {'current_user_name': None}

    return app