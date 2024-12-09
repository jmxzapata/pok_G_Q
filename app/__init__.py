# app/__init__.py
from flask import Flask
from flask_wtf import CSRFProtect
import os

def create_app():
    app = Flask(__name__)
    
    # Genera automáticamente una clave secreta si no está definida en variables de entorno
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    csrf = CSRFProtect(app)

    from .routes import main
    app.register_blueprint(main)

    return app
