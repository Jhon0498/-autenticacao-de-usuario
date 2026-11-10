# Importa o pytest para executar os testes.
import pytest

# Importa a função responsável por criar a aplicação.
from app import create_app

# Importa a extensão do banco de dados.
from app.extensions import db

# Importa o modelo de usuário.
from app.models import User


# Configura a aplicação e o banco de dados para os testes.
@pytest.fixture
def app():
    app = create_app("testing")

    # Desativa o CSRF somente durante os testes.
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with app.app_context():
        # Cria as tabelas no banco de teste.
        db.create_all()

        yield app

        # Limpa a sessão e remove as tabelas de teste.
        db.session.remove()
        db.drop_all()


# Testa se as páginas de login e cadastro abrem.
def test_paginas_autenticacao(app):
    cliente = app.test_client()

    resposta_login = cliente.get("/login")
    resposta_cadastro = cliente.get("/register")

    assert resposta_login.status_code == 200
    assert resposta_cadastro.status_code == 200


# Testa o cadastro de um novo usuário.
def test_cadastro_usuario(app, monkeypatch):

    # Simula o envio do e-mail para não enviar mensagens reais.
    monkeypatch.setattr(
        "app.auth.views.send_email",
        lambda *args, **kwargs: True
    )

    cliente = app.test_client()

    resposta = cliente.post(
        "/register",
        data={
            "email": "teste@example.com",
            "username": "usuario_teste",
            "password": "Senha123",
            "password2": "Senha123"
        }
    )

    assert resposta.status_code == 302

    # Verifica se o usuário foi registrado.
    usuario = User.query.filter_by(
        email="teste@example.com"
    ).first()

    assert usuario is not None
    assert usuario.username == "usuario_teste"
    assert usuario.confirmed is False


# Testa o login com uma senha correta.
def test_login_usuario(app):

    # Cria um usuário para o teste.
    usuario = User(
        email="login@example.com",
        username="usuario_login",
        password="Senha123",
        confirmed=True
    )

    db.session.add(usuario)
    db.session.commit()

    cliente = app.test_client()

    resposta = cliente.post(
        "/login",
        data={
            "email": "login@example.com",
            "password": "Senha123"
        }
    )

    assert resposta.status_code == 302


# Testa a confirmação de uma conta.
def test_confirmacao_usuario(app):

    # Cria um usuário ainda não confirmado.
    usuario = User(
        email="confirmar@example.com",
        username="usuario_confirmar",
        password="Senha123"
    )

    db.session.add(usuario)
    db.session.commit()

    # Gera o token de confirmação.
    token = usuario.generate_confirmation_token()

    cliente = app.test_client()

    # Realiza o login.
    cliente.post(
        "/login",
        data={
            "email": "confirmar@example.com",
            "password": "Senha123"
        }
    )

    # Acessa o link de confirmação.
    resposta = cliente.get(f"/confirm/{token}")

    assert resposta.status_code == 302

    # Verifica se a conta foi confirmada.
    usuario_atualizado = User.query.filter_by(
        email="confirmar@example.com"
    ).first()

    assert usuario_atualizado.confirmed is True
