### Documentação da Estrutura do Projeto: InvestEasy (Back-end)

**Versão:** 1.0
**Data:** 16 de agosto de 2025
**Tecnologia:** Python com Flask

#### 1. Visão Geral

Este documento descreve a organização dos arquivos e diretórios do back-end do projeto InvestEasy. A estrutura foi planejada para ser modular, escalável e organizada, seguindo as melhores práticas de desenvolvimento com o framework Flask. O objetivo é separar as diferentes responsabilidades da aplicação (como rotas, lógica de negócio, acesso a dados) em arquivos distintos, facilitando a manutenção e o desenvolvimento de novas funcionalidades.

#### 2. Estrutura de Diretórios

A estrutura principal do projeto é a seguinte:

InvestEasy/
|
|-- app/
|   |-- init.py
|   |-- routes.py
|   |-- models.py
|   |-- services.py
|   |-- templates/
|   |-- static/
|
|-- venv/
|-- run.py
|-- config.py
|-- requirements.txt
|-- app.db

#### 3. Descrição dos Componentes

##### 3.1. Diretório Raiz (`InvestEasy/`)

Este é o contêiner principal de todo o projeto.

* **`run.py`**
    * **Propósito:** É o ponto de entrada da nossa aplicação. É o arquivo que executamos no terminal (`python run.py`) para iniciar o servidor de desenvolvimento do Flask.
    * **Responsabilidades:**
        * Importar a função `create_app` do pacote `app` para criar a instância da aplicação.
        * Iniciar o servidor web.

* **`config.py`**
    * **Propósito:** Centralizar todas as variáveis de configuração da aplicação.
    * **Responsabilidades:**
        * Armazenar chaves secretas (ex: `SECRET_KEY`), que são essenciais para a segurança da aplicação.
        * Definir a localização e o tipo do banco de dados (ex: `SQLALCHEMY_DATABASE_URI`).
        * Manter outras configurações que podem variar entre ambientes de desenvolvimento e produção.

* **`requirements.txt`**
    * **Propósito:** Listar todas as bibliotecas Python de que o projeto depende.
    * **Responsabilidades:**
        * Garantir que qualquer pessoa que trabalhe no projeto possa instalar exatamente as mesmas versões das dependências com um único comando (`pip install -r requirements.txt`).

* **`venv/`**
    * **Propósito:** Contém o ambiente virtual do Python.
    * **Responsabilidades:**
        * Isolar as bibliotecas e dependências deste projeto, evitando conflitos com outros projetos na mesma máquina.

* **`app.db`** (será criado ao iniciar)
    * **Propósito:** Este é o arquivo do banco de dados SQLite.
    * **Responsabilidades:**
        * Armazenar todos os dados da aplicação, como a tabela de usuários com seus nomes, e-mails e senhas.

##### 3.2. Pacote da Aplicação (`app/`)

Este diretório contém o coração da nossa aplicação Flask.

* **`__init__.py`**
    * **Propósito:** É um arquivo especial que faz duas coisas: transforma o diretório `app/` em um módulo Python (o que nos permite importar arquivos dele) e contém a "fábrica" da nossa aplicação.
    * **Responsabilidades:**
        * Definir a função `create_app()`, que cria e configura a instância principal do Flask.
        * Inicializar as extensões que usaremos, como o banco de dados (`SQLAlchemy`).

* **`routes.py`**
    * **Propósito:** Definir as URLs da nossa API e associá-las a funções Python.
    * **Responsabilidades:**
        * Criar os "endpoints" que o front-end irá chamar. Por exemplo, a rota `/login` receberá os dados de e-mail e senha, e a rota `/calcular/cdb` receberá os dados para a simulação.
        * Orquestrar as respostas para as requisições do cliente.

* **`models.py`**
    * **Propósito:** Definir a estrutura do nosso banco de dados usando classes Python.
    * **Responsabilidades:**
        * Cada classe neste arquivo representa uma tabela no banco de dados. Por exemplo, uma classe `User` definirá as colunas `id`, `nome`, `sobrenome`, `email` e `senha_hash`.
        * O `Flask-SQLAlchemy` usa esses modelos para criar as tabelas e gerenciar os dados.

* **`services.py`**
    * **Propósito:** Isolar a lógica de negócio principal e as interações com serviços externos.
    * **Responsabilidades:**
        * Conter as funções que se comunicam com as APIs do Banco Central e do Tesouro Transparente para buscar os indicadores financeiros.
        * Implementar as fórmulas de cálculo dos investimentos (CDB, Tesouro Selic, etc.).
        * Dessa forma, as `routes.py` permanecem limpas, apenas chamando essas funções de serviço.

* **`templates/`** e **`static/`**
    * **Propósito:** Pastas padrão do Flask. A `templates/` guardaria arquivos HTML e a `static/` guardaria arquivos como CSS, JavaScript e imagens.
    * **Responsabilidades:**
        * No nosso projeto, como o front-end será separado e a interface é primariamente textual, essas pastas terão menos importância, mas é uma boa prática mantê-las na estrutura.