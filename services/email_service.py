
# Importa a biblioteca para realizar requisições HTTP.
import requests

# Importa as configurações atuais da aplicação Flask.
from flask import current_app


# Define a função responsável por enviar o e-mail pelo Mailgun.
def enviar_email_mailgun(username, nome, email_informado=None):

    # Recupera os destinatários configurados na aplicação.
    flasky_admin = current_app.config.get('FLASKY_ADMIN', '')

    # Separa os e-mails configurados por vírgula.
    destinatarios = [
        email.strip()
        for email in flasky_admin.split(',')
        if email.strip()
    ]

    # Adiciona o e-mail informado no formulário, quando existir.
    if email_informado:
        destinatarios.append(email_informado.strip())

    # Remove e-mails repetidos, preservando a ordem.
    destinatarios = list(dict.fromkeys(destinatarios))

    # Recupera as configurações do Mailgun.
    api_key = current_app.config.get('MAILGUN_API_KEY')
    domain = current_app.config.get('MAILGUN_DOMAIN')
    base_url = current_app.config.get('MAILGUN_BASE_URL')

    # Verifica se as configurações obrigatórias existem.
    if not api_key:
        return False, 'A chave do Mailgun não está configurada.'

    if not domain:
        return False, 'O domínio do Mailgun não está configurado.'

    if not base_url:
        return False, 'A URL do Mailgun não está configurada.'

    if not destinatarios:
        return False, 'Nenhum destinatário foi configurado.'

    # Monta o endereço da API do Mailgun.
    url = f'{base_url.rstrip("/")}/v3/{domain}/messages'

    # Define o remetente da mensagem.
    remetente = f'Cadastro de Alunos <postmaster@{domain}>'

    # Define o assunto do e-mail.
    assunto = 'Novo cadastro realizado'

    # Monta a mensagem com o prontuário fixo.
    mensagem_email = (
        'Novo cadastro realizado!\n\n'
        f'Usuário: {username}\n'
        f'Nome do aluno: {nome}\n'
        'Prontuário: PT3026931'
    )

    # Prepara os dados enviados para a API.
    dados = {
        'from': remetente,
        'to': destinatarios,
        'subject': assunto,
        'text': mensagem_email
    }

    try:
        # Envia a mensagem ao Mailgun.
        resposta = requests.post(
            url,
            auth=('api', api_key),
            data=dados,
            timeout=30
        )

        # Verifica se o Mailgun aceitou a solicitação de envio.
        if resposta.status_code in (200, 202):
            return True, {
                'destinatarios': destinatarios,
                'assunto': assunto
            }

        # Registra a falha sem devolver detalhes técnicos à página.
        current_app.logger.error(
            'Falha no Mailgun: status %s',
            resposta.status_code
        )

        return False, 'Não foi possível enviar o e-mail pelo Mailgun.'

    except requests.exceptions.RequestException:
        # Registra a falha de conexão sem expor dados sensíveis.
        current_app.logger.exception(
            'Erro de conexão ao enviar e-mail pelo Mailgun.'
        )

        return False, 'Ocorreu um erro de conexão com o Mailgun.'
