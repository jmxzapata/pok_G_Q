from flask import Flask
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cambiala-por-una-clave-segura'
    csrf = CSRFProtect(app)

    from .routes import main
    app.register_blueprint(main)

    return app
