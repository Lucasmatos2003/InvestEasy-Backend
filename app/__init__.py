# app/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Cria as instâncias das extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    """
    Cria e configura a instância da aplicação Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importa e registra as rotas (URLs) da nossa aplicação
    # A importação é feita aqui para evitar importações circulares
    with app.app_context():
        from . import routes

    return app