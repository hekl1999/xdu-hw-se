from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    cors.init_app(app=app, supports_credentials=True)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from.student import student as student_blueprint

    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    from .root import root as root_blueprint
    app.register_blueprint(root_blueprint, url_prefix='/root')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    return app
