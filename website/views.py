from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import *
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import json
import ast

views = Blueprint('views', __name__)



@views.route('/')
@login_required
def homePage():
    servers = Servers.query.all()
    print(servers)
    hostnames = [server.hostname for server in servers]
    return render_template("main_page.html", user=current_user, servers=servers, hostnames=json.dumps(hostnames))


@views.route('/manage_servers', methods=['GET', 'POST'])
@login_required
def manageServers():
    if request.method == 'POST':
        hostname = request.form.get('serverHostname')

        server = Servers.query.filter_by(hostname=hostname).first()
        if not server:
            new_server = Servers(hostname=hostname)
            db.session.add(new_server)
            db.session.commit()

    servers = Servers.query.all()

    return render_template("manageServers.html", user=current_user, servers=servers)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
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
@login_required
def getServerData(hostname):
    server = Servers.query.filter_by(hostname=hostname).first()

    disks_dict = {}
    for i in range(len(server.disks_measurements)-1, 0, -1):
        if server.disks_measurements[i].disk_id in disks_dict:
            break
        else:
            disks_dict[server.disks_measurements[i].disk_id] = server.disks_measurements[i]

    if len(server.measurements) == 0:
        cpu = 0
        mem = 0

    else:
        cpu = round(server.measurements[-1].cpu_usage_pct)
        mem = round(server.measurements[-1].ram_used_pct)

    total_space = 0
    used_space = 0
    running_services = []
    stopped_services = []
    others_status_services = []
    for disk in disks_dict:
        total_space += int(disks_dict[disk].total_space)
        used_space += int(disks_dict[disk].used_space)

    if total_space == 0:
        storage = 0
    else:
        storage = round(used_space / total_space * 100)
    for service in server.services:
        if service.watched == 1:
            last_change = sorted(service.info, key=lambda x: x.status_change_date, reverse=True)[0]
            if last_change.status == "Stopped":
                stopped_services.append(service.name)
            elif last_change.status == "Running":
                running_services.append(service.name)
            else:
                others_status_services.append(service.name)

    return jsonify({"CPU": cpu,
                    "MEM": mem,
                   "STRG": storage,
                    "running_services": running_services,
                    "stopped_services": stopped_services,
                    "others_status_services": others_status_services})


@views.route('/overview/<hostname>', methods=['GET', 'POST'])
@login_required
def overview(hostname):
    server = Servers.query.filter_by(hostname=hostname).first()

    if request.method == 'POST':
        id = int(request.form.get('serviceID'))
        service = Spec_Service.query.filter_by(id=id).first()
        print(service)
        print(request.form.get('action')[0])
        if request.form.get('action') == 'add':
            service.watched = 1
        elif request.form.get('action') == 'remove':
            service.watched = 0
        db.session.commit()

        print('test')
        print(request.form.to_dict(flat=False))
    if server:
        spec = {'OS': ast.literal_eval(server.specification[-1].os),
                'Motherboard': ast.literal_eval(server.specification[-1].motherboard),
                'CPU': ast.literal_eval(server.specification[-1].cpu),
                'RAM': ast.literal_eval(server.specification[-1].ram),
                'GPU': ast.literal_eval(server.specification[-1].gpu),
                'Disks': ast.literal_eval(server.specification[-1].disk)}

        print(spec)
    return render_template("overview.html", user=current_user, server=server, spec=spec)


@views.route('/get-data', methods=['POST'])
@login_required
def get_data():
    data = json.loads(request.data)
    print(data)

    start_date = datetime.strptime(data['startTime'][:-5], '%Y-%m-%dT%H:%M:%S')
    end_date = datetime.strptime(data['endTime'][:-5], '%Y-%m-%dT%H:%M:%S')

    resoults = {
        "services": [],
        "measurements": {
            "CPU":[],
            "MEM": []
        },
        "spec": {
            'os': '',
            'motherboard': '',
            'cpu': '',
            'ram': '',
            'gpu': '',
            'disk': ''
        }
    }
    server = Servers.query.filter_by(hostname=data['hostname']).first()

    for service in server.services:
        statuses = sorted(service.info, key=lambda x: x.status_change_date, reverse=True)
        if len(statuses) > 0:
            last_status = statuses[0]
            temp_service_info = {
                "name": service.name,
                "status": last_status.status,
                "status_change_date": last_status.status_change_date.strftime("%Y-%m-%d %H:%M")
            }
            resoults['services'].append(temp_service_info)

    measurements = Info_Measurements.query.filter(
        Info_Measurements.server_id == server.id,
        Info_Measurements.measurement_date >= start_date,
        Info_Measurements.measurement_date <= end_date
    ).all()

    disk_measurements = Info_DiskMeasurements.query.filter(
        Info_DiskMeasurements.server_id == server.id,
        Info_DiskMeasurements.measurement_date >= start_date,
        Info_DiskMeasurements.measurement_date <= end_date
    ).all()

    for measurement in measurements:
        resoults['measurements']['CPU'].append({"x": measurement.measurement_date, "y": measurement.cpu_usage_pct})
        resoults['measurements']['MEM'].append({"x": measurement.measurement_date, "y": measurement.ram_used_pct})

    for disk_measurement in disk_measurements:
        if disk_measurement.disk_id not in resoults['measurements']:
            resoults['measurements'][disk_measurement.disk_id] = []
        resoults['measurements'][disk_measurement.disk_id].append(
            {
                "x": disk_measurement.measurement_date,
                "y": round((int(disk_measurement.used_space)/int(disk_measurement.total_space))*100)
            })

    resoults['spec']['os'] = server.specification[-1].os
    resoults['spec']['motherboard'] = server.specification[-1].motherboard
    resoults['spec']['cpu'] = server.specification[-1].cpu
    resoults['spec']['ram'] = server.specification[-1].ram
    resoults['spec']['gpu'] = server.specification[-1].gpu
    resoults['spec']['disk'] = server.specification[-1].disk

    return jsonify(resoults)


@views.route('/remove-server', methods=['POST'])
@login_required
def remove_server():
    server_id = int(request.form.get('serverID'))
    server = Servers.query.filter_by(id=server_id).first()
    server.remove = 1
    db.session.commit()

    return redirect(url_for('views.manageServers'))
