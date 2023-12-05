from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

login_manager = LoginManager()
db = SQLAlchemy()
DB_NAME = "WMI.db"
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DATABASE_PATH = os.path.join(PARENT_DIR, f'instance/{DB_NAME}')


def create_app():

    app.config['SECRET_KEY'] = 'GQS_FjMkfVh-DLX9NrfLU2'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    from .models import User
    create_database(app)

    return (app, db)


def create_database(app):
    from .models import User
    if not os.path.exists(DATABASE_PATH):
        print(DATABASE_PATH)
        with app.app_context():
            db.create_all()
            new_user = User(username='adminWMI',
                            password=generate_password_hash('adminWMI', method='scrypt'),
                            account_type='Admin',
                            reset_password=False)
            new_user.generate_api_key()
            db.session.add(new_user)
            db.session.commit()
            print('Database created...')
