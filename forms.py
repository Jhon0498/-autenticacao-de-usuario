
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class FormularioAluno(FlaskForm):

    # Nome do usuário
    usuario = StringField(
        'Qual é o seu nome?:',
        validators=[DataRequired()]
    )

    # E-mail para envio de notificação do novo usuário
    email = StringField(
        'Qual é o seu email (Envio de notificação do novo usuário)?',
        validators=[DataRequired(), Email()],
        render_kw={
            'placeholder': 'Digite seu e-mail'
        }
    )

    # Prontuário do usuário
    prontuario = StringField(
        'Qual é o seu prontuário?:',
        validators=[DataRequired()],
        default='PT3026931'
    )

    # Checkbox para escolher se deseja enviar e-mail
    enviar_email = BooleanField(
        'Deseja enviar e-mail para flaskaulasweb@zohomail.com?'
    )

    # Botão que envia o formulário
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    # Campo de e-mail
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={
            'placeholder': 'Email'
        }
    )

    # Campo de senha
    senha = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Password',
        }
    )

    # Opção para manter o usuário conectado
    remember_me = BooleanField('Keep me logged in')

    # Botão de envio
    submit = SubmitField('Log In')
