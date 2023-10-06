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
    return render_template("/login.html", user=current_user)