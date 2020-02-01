import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_admin import Admin

from config import config
import logging

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
bootstrap = Bootstrap()
admin = Admin(name='ver_flask', template_mode='bootstrap3')

env_name = os.getenv('FLASK_ENV', 'default')
config_name = os.getenv('FLASK_CONFIG', env_name)

def create_app(config_class=config[config_name]):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
   
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


logging.basicConfig(filename='log.log')

from app import models
from app.main import routes, admin_views
