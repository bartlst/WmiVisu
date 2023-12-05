from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import send_from_directory
import os

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.homePage'))
    if request.method == 'POST':
        print(request.form.to_dict())
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                print('login!')
                return redirect(url_for('views.homePage'))
    return render_template("/login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))