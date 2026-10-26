# Flask Application Factory

Aplicação web desenvolvida com Flask, organizada com o padrão **Application Factory**, Blueprints e separação de responsabilidades. O projeto demonstra uma estrutura modular para facilitar a manutenção, os testes e a evolução da aplicação.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bootstrap
- Flask-Moment
- SQLite
- Pytest

## Estrutura do projeto

```text
flask-application-factory-ok/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
├── main/
│   ├── __init__.py
│   ├── errors.py
│   └── views.py
├── migrations/
│   └── versions/
├── static/
├── templates/
├── tests/
│   └── test_app.py
├── config.py
├── flasky.py
├── forms.py
├── requirements.txt
└── .gitignore
```

## Funcionalidades

- Cadastro e consulta de usuários.
- Registro de informações de e-mails enviados.
- Integração com banco de dados por meio do SQLAlchemy.
- Gerenciamento de alterações no banco com Flask-Migrate.
- Organização das rotas utilizando Blueprints.
- Tratamento de erros HTTP 404 e 500.
- Testes automatizados com Pytest.

## Organização da aplicação

**Application Factory:** a função `create_app()` centraliza a criação e a configuração da aplicação Flask.

**Blueprints:** as rotas e os tratamentos de erros são organizados em módulos separados.

**Extensões:** as integrações com banco de dados, migrações e bibliotecas auxiliares são inicializadas em `app/extensions.py`.

**Configurações:** o arquivo `config.py` reúne configurações para diferentes ambientes, como desenvolvimento, testes e produção.

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Jhon0498/flask-application-factory-ok.git
cd flask-application-factory-ok
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

Ativar no Windows:

```bash
venv\Scripts\activate
```

Ativar no Linux ou macOS:

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` conforme as configurações necessárias no projeto. Defina a chave secreta e os parâmetros de conexão com o banco de dados. Não publique senhas, tokens ou outras credenciais no GitHub.

### 5. Executar a aplicação

```bash
python flasky.py
```

O endereço local padrão do Flask é:

```text
http://127.0.0.1:5000
```

## Testes

Para executar os testes automatizados:

```bash
python -m pytest -v tests/
```

## Objetivo do projeto

Praticar a organização de aplicações Flask por meio de uma arquitetura modular, utilizando Application Factory, Blueprints, configurações separadas, extensões reutilizáveis e testes automatizados.

## Autor

Jhonatan Mendes Morão

## Licença

Projeto desenvolvido para fins educacionais.
