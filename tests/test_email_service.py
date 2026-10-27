
# Importa o pytest para executar os testes.
import pytest

# Importa a função que será testada.
from services.email_service import enviar_email_mailgun

# Importa a função que cria a aplicação Flask.
from app import create_app


# Cria uma aplicação de teste para os testes deste arquivo.
@pytest.fixture
def app():
    # Utiliza as configurações próprias para testes.
    return create_app("testing")


# Testa o envio de e-mail sem enviar uma mensagem real.
def test_envio_email_mailgun(monkeypatch, app):
    # Configura valores fictícios para o Mailgun.
    app.config["MAILGUN_API_KEY"] = "chave-de-teste"
    app.config["MAILGUN_DOMAIN"] = "teste.example.com"
    app.config["MAILGUN_BASE_URL"] = "https://api.mailgun.net"
    app.config["FLASKY_ADMIN"] = "institucional@example.com"

    # Guarda os dados que seriam enviados ao Mailgun.
    requisicao = {}

    # Simula uma resposta de sucesso do Mailgun.
    class RespostaFalsa:
        status_code = 200

    # Substitui a requisição real por uma simulação.
    def post_falso(url, auth, data, timeout):
        requisicao["url"] = url
        requisicao["auth"] = auth
        requisicao["data"] = data
        requisicao["timeout"] = timeout
        return RespostaFalsa()

    # Faz o teste utilizar a requisição simulada.
    monkeypatch.setattr(
        "services.email_service.requests.post",
        post_falso
    )

    # Ativa o contexto necessário para acessar as configurações.
    with app.app_context():
        # Executa a função de envio com dados fictícios.
        sucesso, resultado = enviar_email_mailgun(
            username="aluno",
            nome="Aluno Teste",
            email_informado="aluno@example.com"
        )

    # Confirma que o envio simulado foi bem-sucedido.
    assert sucesso is True

    # Confirma que o destinatário institucional foi incluído.
    assert "institucional@example.com" in resultado["destinatarios"]

    # Confirma que o e-mail informado também foi incluído.
    assert "aluno@example.com" in resultado["destinatarios"]

    # Confirma que o prontuário está na mensagem.
    assert "PT3026931" in requisicao["data"]["text"]

    # Confirma que o endereço da API foi montado corretamente.
    assert requisicao["url"] == (
        "https://api.mailgun.net/v3/teste.example.com/messages"
    )

    # Confirma que a autenticação foi configurada corretamente.
    assert requisicao["auth"] == ("api", "chave-de-teste")


# Testa o tratamento de uma falha retornada pelo Mailgun.
def test_falha_mailgun(monkeypatch, app):
    # Configura valores fictícios para o Mailgun.
    app.config["MAILGUN_API_KEY"] = "chave-de-teste"
    app.config["MAILGUN_DOMAIN"] = "teste.example.com"
    app.config["MAILGUN_BASE_URL"] = "https://api.mailgun.net"
    app.config["FLASKY_ADMIN"] = "institucional@example.com"

    # Simula uma resposta de erro do Mailgun.
    class RespostaFalsa:
        status_code = 400

    # Substitui a requisição real por uma resposta de erro simulada.
    monkeypatch.setattr(
        "services.email_service.requests.post",
        lambda *args, **kwargs: RespostaFalsa()
    )

    # Ativa o contexto necessário para acessar as configurações.
    with app.app_context():
        # Executa a função de envio.
        sucesso, mensagem = enviar_email_mailgun(
            username="aluno",
            nome="Aluno Teste"
        )

    # Confirma que a função identificou a falha.
    assert sucesso is False

    # Confirma que a mensagem de erro esperada foi retornada.
    assert "Não foi possível enviar" in mensagem

 
