# app/routes.py

from flask import current_app, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

@current_app.route('/api')
def api_index():
    return jsonify({'mensagem': 'API do InvestEasy está no ar!'})


# --- ROTAS DE AUTENTICAÇÃO ---

@current_app.route('/api/registrar', methods=['POST'])
def registrar_usuario():
    dados = request.get_json()

    if not dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({'erro': 'Dados incompletos fornecidos'}), 400

    if User.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'Este e-mail já está em uso'}), 409

    novo_usuario = User(
        primeiro_nome=dados.get('primeiro_nome'),
        sobrenome=dados.get('sobrenome'),
        email=dados['email']
    )
    novo_usuario.set_password(dados['senha'])
    
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201


@current_app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()

    if not dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({'erro': 'E-mail ou senha não fornecidos'}), 400

    usuario = User.query.filter_by(email=dados['email']).first()

    if usuario is None or not usuario.check_password(dados['senha']):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    # Gera o token de acesso que será usado pelo front-end
    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token)


@current_app.route('/api/recuperar-senha', methods=['POST'])
def recuperar_senha():
    dados = request.get_json()

    if not dados or not 'email' in dados:
        return jsonify({'erro': 'E-mail não fornecido'}), 400
    
    usuario = User.query.filter_by(email=dados['email']).first()

    if usuario:
        # TODO: Implementar envio de e-mail com token de recuperação.
        print(f"DEBUG: E-mail de recuperação seria enviado para {usuario.email}")
    
    mensagem_sucesso = 'Se o e-mail estiver em nosso sistema, um link de recuperação será enviado.'
    return jsonify({'mensagem': mensagem_sucesso})