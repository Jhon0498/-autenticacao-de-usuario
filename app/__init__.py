
# Importa recursos para criar a aplicação Flask.
from flask import Flask

# Importa as configurações dos ambientes.
from config import config

# Importa as extensões compartilhadas.
from app.extensions import db, migrate, bootstrap, moment, login_manager


# Cria e configura a aplicação.
def create_app(config_name="default"):
    # Define os caminhos dos templates e arquivos estáticos.
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    # Carrega as configurações escolhidas.
    app.config.from_object(
        config.get(config_name, config["default"])
    )

    # Inicializa as extensões.
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    # Define a página de login para usuários não autenticados.
    login_manager.login_view = 'main.login'

    # Registra os modelos do banco de dados.
    from app import models

    # Importa e registra as rotas.
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Retorna a aplicação pronta.
    return app
