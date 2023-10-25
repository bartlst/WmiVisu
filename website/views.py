from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Servers, User, Info_Service, Info_Measurements
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import json

views = Blueprint('views', __name__)



@views.route('/')
def homePage():
    servers = Servers.query.all()
    print(servers)
    hostnames = [server.hostname for server in servers]
    return render_template("main_page.html", user=current_user, servers=servers, hostnames=json.dumps(hostnames))


@views.route('/manage_servers', methods=['GET', 'POST'])
def manageServers():
    if request.method == 'POST':
        print(request.form.to_dict(flat=False))
        hostname = request.form.get('serverHostname')
        ipAddress = request.form.get('serverIpAddress')

        server = Servers.query.filter_by(hostname=hostname).first()
        if not server:
            new_server = Servers(hostname=hostname, ip_address=ipAddress)
            db.session.add(new_server)
            db.session.commit()

    return render_template("manageServers.html", user=current_user)


@views.route('/settings', methods=['GET', 'POST'])
def appSettings():
    if request.method == 'POST':
        print(request.form.to_dict(flat=False))

    if request.method == 'POST':
        if request.form.get('formType') == 'addNewUser':
            username = request.form.get('username')
            password = request.form.get('password')
            accountType = request.form.get('accountType')
            user = User.query.filter_by(username=username).first()
            if not user:
                new_user = User(username=username,
                                password=generate_password_hash(password, method='scrypt'),
                                account_type=accountType,
                                reset_password=True)
                db.session.add(new_user)
                db.session.commit()
    return render_template("setting_page.html", user=current_user)

@views.route('/getServerData/<hostname>')
def getServerData(hostname):
    server = Servers.query.filter_by(hostname=hostname).first()
    print("CPU:",round(server.measurements[-1].cpu_usage_pct))
    print("MEM:",round(server.measurements[-1].ram_used_pct))
    disks_dict = {}
    for i in range(len(server.disks)-1, 0, -1):
        if server.disks[i].disk_id in disks_dict:
            break
        else:
            disks_dict[server.disks[i].disk_id] = server.disks[i]

    total_space = 0
    used_space = 0
    for disk in disks_dict:
        total_space+=disks_dict[disk].total_space
        used_space+=disks_dict[disk].used_space
    print("STRG:",round(used_space/total_space*100))
    return jsonify({"CPU":round(server.measurements[-1].cpu_usage_pct),
                    "MEM":round(server.measurements[-1].ram_used_pct),
                   "STRG":round(used_space/total_space*100)})
