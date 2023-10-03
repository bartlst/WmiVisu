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


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         if 'login_email' in request.form.keys():
#             print("LOGOWANIE")
#             email = request.form.get('login_email')
#             password = request.form.get('login_password')
#
#             user = User.query.filter_by(email=email).first()
#             if user:
#                 if check_password_hash(user.password, password):
#                     login_user(user)
#                     if user.reset_password:
#                         return render_template("/password_reset.html", user=current_user)
#                     else:
#                         print(f"User with email {email} logged in")
#
#                         return redirect(url_for('views.proj_list'))
#                 else:
#                     print('flash!')
#                     flash("Incorrect password try again", "Error-password")
#             else:
#                 print('flash!')
#                 flash("User with that email is not registered", "Error-email")
#         elif 'reset_password' in request.form.keys():
#             print("RESETOWANIE")
#             password = request.form.get('reset_password')
#             user = User.query.filter_by(id=current_user.id).first()
#             user.password = generate_password_hash(password, method='scrypt')
#             user.reset_password = False
#             db.session.commit()
#             return redirect(url_for('views.proj_list'))
#     if current_user.is_authenticated:
#         if current_user.reset_password:
#             return render_template("/password_reset.html", user=current_user)
#     return render_template("/base.html", user=current_user)