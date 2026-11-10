from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Cria a instância do SQLAlchemy sem associá-la a uma aplicação específica.
db = SQLAlchemy()

# Cria a instância responsável pelas migrações do banco de dados.
migrate = Migrate()

# Cria a instância responsável pelos recursos do Bootstrap.
bootstrap = Bootstrap()

# Cria a instância responsável pela exibição de datas e horários.
moment = Moment()

# Cria a instância responsável pela autenticação dos usuários.
login_manager = LoginManager()
