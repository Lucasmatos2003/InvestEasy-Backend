# app/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

# Cria a instância do banco de dados, mas ainda não a vincula à aplicação.
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Cria e configura a instância da aplicação Flask.
    """
    # Cria a aplicação Flask.
    app = Flask(__name__)
    
    # Carrega as configurações a partir da classe Config.
    app.config.from_object(config_class)

    # Inicializa o banco de dados com a aplicação.
    db.init_app(app)

    # Importa e registra as rotas (URLs) da nossa aplicação.
    # A importação é feita aqui para evitar importações circulares.
    from app import routes, models
    
    return app