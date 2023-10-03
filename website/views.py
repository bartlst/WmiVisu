from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import json

views = Blueprint('views', __name__)



@views.route('/')
def homePage():
    return render_template("base.html")


@views.route('/manage_servers')
def manageServers():
    return render_template("manageServers.html")