# app/routes.py

from flask import current_app

@current_app.route('/')
@current_app.route('/index')
def index():
    """
    Rota principal da aplicação.
    Retorna uma mensagem de boas-vindas.
    """
    return "Bem-vindo ao back-end do InvestEasy!"