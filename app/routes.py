# app/routes.py

from flask import current_app, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import services

# --- ROTA DE TESTE ---

@current_app.route('/api')
def api_index():
    """Rota de teste para verificar se a API está no ar."""
    return jsonify({'mensagem': 'API do InvestEasy está no ar!'})


# --- ROTAS DE AUTENTICAÇÃO ---

@current_app.route('/api/registrar', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para registrar um novo usuário.
    Espera um JSON com: primeiro_nome, sobrenome, email, senha.
    """
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
    """
    Endpoint para login de usuário.
    Espera um JSON com: email, senha.
    Retorna um token de acesso JWT em caso de sucesso.
    """
    dados = request.get_json()

    if not dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({'erro': 'E-mail ou senha não fornecidos'}), 400

    usuario = User.query.filter_by(email=dados['email']).first()

    if usuario is None or not usuario.check_password(dados['senha']):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    # Gera o token de acesso que será usado pelo front-end para autenticar requisições futuras
    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token)


@current_app.route('/api/recuperar-senha', methods=['POST'])
def recuperar_senha():
    """
    Endpoint para solicitar a recuperação de senha.
    Espera um JSON com: email.
    """
    dados = request.get_json()

    if not dados or not 'email' in dados:
        return jsonify({'erro': 'E-mail não fornecido'}), 400
    
    usuario = User.query.filter_by(email=dados['email']).first()

    if usuario:
        # TODO: Implementar lógica de envio de e-mail com token de recuperação.
        print(f"DEBUG: E-mail de recuperação seria enviado para {usuario.email}")
    
    # Mensagem genérica para não revelar se um e-mail existe no sistema
    mensagem_sucesso = 'Se o e-mail estiver em nosso sistema, um link de recuperação será enviado.'
    return jsonify({'mensagem': mensagem_sucesso})


# --- ROTAS DE DADOS E SIMULAÇÕES ---

@current_app.route('/api/indicadores', methods=['GET'])
def get_indicadores():
    """
    Endpoint público para buscar os indicadores de mercado atuais (CDI e Selic).
    """
    dados = services.get_indicadores_mercado()
    if "erro" in dados:
        return jsonify(dados), 503 # Service Unavailable
    return jsonify(dados)


@current_app.route('/api/simular/cdb', methods=['POST'])
@jwt_required() # Protege a rota, exigindo um token de login válido
def simular_investimento_cdb():
    """
    Endpoint para simular um investimento em CDB.
    Exige autenticação.
    Espera JSON com: valor_inicial, prazo_dias, percentual_cdi.
    """
    dados_entrada = request.get_json()

    if not dados_entrada or not all(k in dados_entrada for k in ('valor_inicial', 'prazo_dias', 'percentual_cdi')):
        return jsonify({"erro": "Parâmetros 'valor_inicial', 'prazo_dias' e 'percentual_cdi' são obrigatórios."}), 400

    try:
        valor = float(dados_entrada['valor_inicial'])
        dias = int(dados_entrada['prazo_dias'])
        percentual = float(dados_entrada['percentual_cdi'])
    except (ValueError, TypeError):
        return jsonify({"erro": "Parâmetros inválidos. Verifique os tipos de dados."}), 400

    usuario_atual_id = get_jwt_identity()
    print(f"Simulação solicitada pelo usuário com ID: {usuario_atual_id}")

    resultado = services.simular_cdb(valor, dias, percentual)

    if "erro" in resultado:
        return jsonify(resultado), 503
    
    return jsonify(resultado)

# TODO: Adicionar rotas para LCI/LCA e Tesouro Direto
# @current_app.route('/api/simular/lci-lca', methods=['POST'])
# @jwt_required()
# def simular_investimento_lci_lca():
#     pass

# @current_app.route('/api/simular/tesouro', methods=['POST'])
# @jwt_required()
# def simular_investimento_tesouro():
#     pass