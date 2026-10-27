# Importa as funções necessárias para criar páginas e acessar a requisição.
from flask import render_template, request, current_app

# Importa recursos para trabalhar com datas e horários.
from datetime import datetime

# Importa o formulário de cadastro existente.
from forms import FormularioAluno

# Importa os modelos da aplicação.
from app.models import User, Role, EmailEnviado

# Importa a instância compartilhada do banco de dados.
from app.extensions import db
from services.email_service import enviar_email_mailgun

# Importa a biblioteca utilizada para enviar requisições ao Mailgun.

# Importa o Blueprint principal da aplicação.
from main import main


# Rota principal do sistema.
# Aceita requisições GET e POST.
@main.route('/', methods=['GET', 'POST'])
def index():

    # Cria uma instância do formulário.
    form = FormularioAluno()

    # Diagnóstico temporário para verificar os dados recebidos.
    print('MÉTODO:', request.method)
    print('DADOS:', request.form)

    # Busca todos os usuários cadastrados no banco.
    usuarios_banco = User.query.all()

    # Verifica se o formulário foi enviado.
    if request.method == 'POST':

        # Valida os campos do formulário, incluindo o e-mail.
        if not form.validate():

            # Mostra a página com os erros de validação.
            return render_template(
                'index.html',
                form=form,
                nome='',
                mensagem='Verifique os campos preenchidos.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Pega o nome digitado no formulário.
        nome = (
            form.usuario.data.strip()
            if form.usuario.data
            else ''
        )

        # Recupera o e-mail informado no formulário.
        email_informado = (
            form.email.data.strip()
            if form.email.data
            else ''
        )

        # Cria um username a partir do nome.
        username = nome.lower().replace(' ', '')

        # Verifica se o usuário já existe.
        usuario_existente = User.query.filter(
            User.username.ilike(username)
        ).first()

        # Impede o cadastro duplicado.
        if usuario_existente:

            return render_template(
                'index.html',
                form=form,
                nome=usuario_existente.name,
                mensagem='Este usuário já está cadastrado.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Busca a função padrão User.
        funcao_user = Role.query.filter_by(
            name='User'
        ).first()

        # Verifica se a função padrão existe.
        if not funcao_user:

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro: a função User não foi encontrada no banco.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Cria um novo usuário com a função User.
        novo_usuario = User(
            username=username,
            name=nome,
            role=funcao_user
        )

        try:

            # Adiciona o usuário à sessão do banco.
            db.session.add(novo_usuario)

            # Salva o usuário no banco de dados.
            db.session.commit()

            # Diagnóstico temporário para confirmar o cadastro.
            print(
                'USUÁRIO SALVO:',
                novo_usuario.id,
                novo_usuario.username,
                novo_usuario.name
            )

        except Exception as erro:

            # Desfaz a operação caso ocorra algum erro.
            db.session.rollback()

            # Mostra o erro no log.
            print('ERRO AO SALVAR USUÁRIO:', erro)

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro ao cadastrar o usuário.',
                users=User.query.all(),
                current_time=datetime.utcnow()
            )

        # Atualiza a relação de usuários após o cadastro.
        usuarios_banco = User.query.all()

        # Envia a notificação usando o serviço separado.
        sucesso_email, resultado_email = enviar_email_mailgun(
            username=username,
            nome=nome,
            email_informado=email_informado
        )

        # Registra o envio quando o Mailgun aceita a solicitação.
        if sucesso_email:
            try:
                # Cria o registro do e-mail enviado.
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

                # Salva o registro no banco de dados.
                db.session.add(novo_email)
                db.session.commit()

            except Exception:
                # Desfaz somente a operação de registro do e-mail.
                db.session.rollback()

                # Registra o erro para diagnóstico.
                current_app.logger.exception(
                    'Erro ao registrar o e-mail no banco.'
                )

            # Informa que o Mailgun aceitou a solicitação.
            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Usuário cadastrado e notificação aceita pelo Mailgun.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Informa que o cadastro ocorreu, mas o envio falhou.
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

    # Exibe a página normalmente quando a requisição é GET.
    return render_template(
        'index.html',
        form=form,
        users=usuarios_banco,
        current_time=datetime.utcnow()
    )


# Rota para visualizar os e-mails enviados.
@main.route('/emails-enviados')
def emails_enviados():

    # Busca os e-mails enviados do mais recente para o mais antigo.
    emails = EmailEnviado.query.order_by(
        EmailEnviado.data_envio.desc()
    ).all()

    # Exibe a página de e-mails enviados.
    return render_template(
        'emails_enviados.html',
        emails=emails
    )
