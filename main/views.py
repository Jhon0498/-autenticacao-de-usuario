
# Importa as funções necessárias do Flask.
from flask import (
    render_template,
    request,
    current_app,
    redirect,
    url_for,
    abort
)

# Importa recursos para trabalhar com datas.
from datetime import datetime

# Importa o formulário de cadastro.
from forms import FormularioAluno

# Importa os modelos da aplicação.
from app.models import User, Role, EmailEnviado

# Importa a instância compartilhada do banco.
from app.extensions import db

# Importa o serviço de envio de e-mails.
from services.email_service import enviar_email_mailgun

# Importa o Blueprint principal.
from main import main


# Rota principal para cadastrar e listar usuários.
@main.route('/', methods=['GET', 'POST'])
def index():

    form = FormularioAluno()
    usuarios_banco = User.query.all()

    if request.method == 'POST':

        if not form.validate():
            return render_template(
                'index.html',
                form=form,
                nome='',
                mensagem='Verifique os campos preenchidos.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        nome = (
            form.usuario.data.strip()
            if form.usuario.data
            else ''
        )

        email_informado = (
            form.email.data.strip()
            if form.email.data
            else ''
        )

        username = nome.lower().replace(' ', '')

        # Verifica se o usuário já existe.
        usuario_existente = User.query.filter(
            User.username.ilike(username)
        ).first()

        if usuario_existente:
            return render_template(
                'index.html',
                form=form,
                nome=usuario_existente.name,
                mensagem='Este usuário já está cadastrado.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Busca a função padrão.
        funcao_user = Role.query.filter_by(
            name='User'
        ).first()

        if not funcao_user:
            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro: a função User não foi encontrada no banco.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Cria o novo usuário.
        novo_usuario = User(
            username=username,
            name=nome,
            role=funcao_user
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()

        except Exception:
            db.session.rollback()

            current_app.logger.exception(
                'Erro ao cadastrar usuário.'
            )

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro ao cadastrar o usuário.',
                users=User.query.all(),
                current_time=datetime.utcnow()
            )

        usuarios_banco = User.query.all()

        # Envia a notificação por e-mail.
        sucesso_email, resultado_email = enviar_email_mailgun(
            username=username,
            nome=nome,
            email_informado=email_informado
        )

        if sucesso_email:
            try:
                novo_email = EmailEnviado(
                    username=username,
                    nome=nome,
                    prontuario='PT3026931',
                    destinatario=', '.join(
                        resultado_email['destinatarios']
                    ),
                    assunto=resultado_email['assunto'],
                    status='Enviado'
                )

                db.session.add(novo_email)
                db.session.commit()

            except Exception:
                db.session.rollback()

                current_app.logger.exception(
                    'Erro ao registrar o e-mail no banco.'
                )

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Usuário cadastrado e notificação aceita pelo Mailgun.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        return render_template(
            'index.html',
            form=form,
            nome=nome,
            mensagem=(
                'Usuário cadastrado, mas não foi possível enviar o e-mail: '
                f'{resultado_email}'
            ),
            users=usuarios_banco,
            current_time=datetime.utcnow()
        )

    return render_template(
        'index.html',
        form=form,
        users=usuarios_banco,
        current_time=datetime.utcnow()
    )


# Rota para visualizar os e-mails enviados.
@main.route('/emails-enviados')
def emails_enviados():

    emails = EmailEnviado.query.order_by(
        EmailEnviado.data_envio.desc()
    ).all()

    return render_template(
        'emails_enviados.html',
        emails=emails
    )


