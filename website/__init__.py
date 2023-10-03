from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from os import path


login_manager = LoginManager()
db = SQLAlchemy()
DB_NAME = "WMI.db"
app = Flask(__name__)


def create_app():

    app.config['SECRET_KEY'] = 'GQS_FjMkfVh-DLX9NrfLU2'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    create_database(app)

    return app


def create_database(app):
    from .models import User
    if not path.exists(f'instance/{DB_NAME}'):
        with app.app_context():
            db.create_all()
            # new_user = User(email='admin@admin',
            #                 password=generate_password_hash('admin', method='scrypt'),
            #                 account_type='Admin',
            #                 reset_password=False)
            # db.session.add(new_user)
            # db.session.commit()
            print('Database created...')
