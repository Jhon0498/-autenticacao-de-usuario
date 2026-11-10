from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(128), nullable=True)
    prontuario = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128), nullable=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


class EmailEnviado(db.Model):
    __tablename__ = 'emails_enviados'

    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(64), nullable=False)
    nome = db.Column(db.String(128), nullable=False)
    prontuario = db.Column(db.String(64), nullable=True)
    destinatario = db.Column(db.Text, nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))