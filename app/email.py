
# Importa recursos necessários do Flask.
from flask import current_app, render_template

# Importa a biblioteca para realizar requisições HTTP.
import requests


# Envia e-mails utilizando a API do Mailgun.
def send_email(to, subject, template, **kwargs):

    # Recupera as configurações do Mailgun.
    api_key = current_app.config.get('MAILGUN_API_KEY')
    domain = current_app.config.get('MAILGUN_DOMAIN')
    base_url = current_app.config.get(
        'MAILGUN_BASE_URL',
        'https://api.mailgun.net'
    )

    # Verifica se as configurações necessárias existem.
    if not api_key or not domain:
        current_app.logger.error('Configurações do Mailgun ausentes.')
        return False

    # Monta o conteúdo HTML do e-mail.
    html = render_template(template + '.html', **kwargs)

    # Define o endereço de envio.
    remetente = f'Flasky <postmaster@{domain}>'

    # Envia a mensagem pela API do Mailgun.
    resposta = requests.post(
        f'{base_url}/v3/{domain}/messages',
        auth=('api', api_key),
        data={
            'from': remetente,
            'to': to,
            'subject': subject,
            'html': html
        }
    )

    # Registra erros caso o envio não seja aceito.
    if resposta.status_code != 200:
        current_app.logger.error(
            'Erro ao enviar e-mail: %s',
            resposta.text
        )
        return False

    return True
