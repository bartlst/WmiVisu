from flask import Blueprint, request, jsonify, abort
from .models import *
from datetime import datetime
from sqlalchemy import cast, String, func

api = Blueprint('api', __name__)


def verify_api_key():
    api_key = request.headers.get('API-KEY')
    if not api_key or not User.query.filter_by(api_key=api_key).first():
        abort(401, 'Invalid API key')


@api.route('/notifications', methods=['GET'])
def get_notifcations():
    query = Notification.query

    record_id = request.args.get('id')
    content = request.args.get('content')
    server_id = request.args.get('server_id')
    cause_type = request.args.get('cause_type')
    resolved = request.args.get('resolved')
    date = request.args.get('date')

    if record_id:
        query = query.filter(Notification.id == record_id)
    if content:
        query = query.filter(cast(Notification.content, String).like(f"%{content}%"))
    if server_id:
        query = query.filter(Notification.server_id == server_id)
    if cause_type:
        query = query.filter(Notification.cause_type == cause_type)
    if resolved:
        query = query.filter(Notification.resolved == resolved)
    if date:
        query = query.filter(cast(Notification.date, String).like(f"%{date}%"))

    notifications = query.all()

    return jsonify([notification.to_dict() for notification in notifications]), 200


@api.route('/servers', methods=['GET'])
def get_servers():
    query = Servers.query

    # Filtrowanie id, jeśli parametr jest podany
    server_id = request.args.get('id')
    hostname = request.args.get('hostname')
    connection_status = request.args.get('connection_status')

    if server_id:
        query = query.filter(Servers.id == server_id)
    if hostname:
        query = query.filter(Servers.hostname == hostname)
    if hostname:
        query = query.filter(Servers.connection_status == connection_status)

    servers = query.all()
    return jsonify([server.to_dict() for server in servers]), 200


@api.route('/measurements', methods=['GET'])
def get_measurements():
    query = Info_Measurements.query

    # Filtrowanie po server_id, jeśli parametr jest podany
    server_id = request.args.get('server_id')
    measurement_date = request.args.get('measurement_date')
    cpu_usage_pct_min = request.args.get('cpu_usage_pct_min')
    cpu_usage_pct_max = request.args.get('cpu_usage_pct_max')
    ram_used_pct_min = request.args.get('ram_used_pct_min')
    ram_used_pct_max = request.args.get('ram_used_pct_max')

    if server_id:
        query = query.filter(Info_Measurements.server_id == server_id)
    if measurement_date:
        # Użycie operatora like dla daty
        query = query.filter(cast(Info_Measurements.measurement_date, String).like(f"%{measurement_date}%"))
    if cpu_usage_pct_min:
        query = query.filter(Info_Measurements.cpu_usage_pct >= float(cpu_usage_pct_min))
    if cpu_usage_pct_max:
        query = query.filter(Info_Measurements.cpu_usage_pct <= float(cpu_usage_pct_max))
    if ram_used_pct_min:
        query = query.filter(Info_Measurements.ram_used_pct >= float(ram_used_pct_min))
    if ram_used_pct_max:
        query = query.filter(Info_Measurements.ram_used_pct <= float(ram_used_pct_max))

    measurements = query.all()
    return jsonify([measurement.to_dict() for measurement in measurements]), 200


@api.route('/disk_measurements', methods=['GET'])
def get_disk_measurements():
    query = Info_DiskMeasurements.query

    # Filtrowanie po server_id, jeśli parametr jest podany
    server_id = request.args.get('server_id')
    total_space = request.args.get('total_space')
    total_space_min = request.args.get('total_space_min')
    total_space_max = request.args.get('total_space_max')
    free_space = request.args.get('free_space')
    free_space_min = request.args.get('free_space')
    free_space_max = request.args.get('free_space')
    used_space = request.args.get('used_space')
    used_space_min = request.args.get('used_space')
    used_space_max = request.args.get('used_space')
    measurement_date = request.args.get('measurement_date')
    disk_id = request.args.get('disk_id')

    if server_id:
        query = query.filter(Info_DiskMeasurements.server_id == server_id)
    if measurement_date:
        query = query.filter(cast(Info_DiskMeasurements.measurement_date, String).like(f"%{measurement_date}%"))
    if disk_id:
        query = query.filter(Info_DiskMeasurements.disk_id.like(f"%{disk_id}%"))

    if total_space:
        query = query.filter(Info_DiskMeasurements.total_space == int(total_space))
    if total_space_min:
        query = query.filter(Info_DiskMeasurements.total_space >= float(total_space_min))
    if total_space_max:
        query = query.filter(Info_DiskMeasurements.total_space <= float(total_space_max))

    if free_space:
        query = query.filter(Info_DiskMeasurements.free_space == int(free_space))
    if free_space_min:
        query = query.filter(Info_DiskMeasurements.free_space >= float(free_space_min))
    if free_space_max:
        query = query.filter(Info_DiskMeasurements.free_space <= float(free_space_max))

    if used_space:
        query = query.filter(Info_DiskMeasurements.used_space == int(used_space))
    if used_space_min:
        query = query.filter(Info_DiskMeasurements.used_space >= float(used_space_min))
    if used_space_max:
        query = query.filter(Info_DiskMeasurements.used_space <= float(used_space_max))

    measurements = query.all()
    return jsonify([measurement.to_dict() for measurement in measurements]), 200


@api.route('/services', methods=['GET'])
def get_services():
    query = Spec_Service.query

    server_id = request.args.get('server_id')
    like_name = request.args.get('like_name')
    name = request.args.get('name')
    watched = request.args.get('watched')

    if server_id:
        query = query.filter(Spec_Service.server_id == server_id)
    if like_name:
        query = query.filter(cast(Spec_Service.name, String).like(f"%{like_name}%"))
    if name:
        query = query.filter(Spec_Service.name == name)
    if watched:
        query = query.filter(Spec_Service.watched == watched)

    services = query.all()

    return jsonify([service.to_dict() for service in services]), 200


@api.route('/services_status', methods=['GET'])
def get_services_status():
    query = Info_Service.query

    record_id = request.args.get('id')
    service_id = request.args.get('service_id')
    status = request.args.get('status')
    status_change_date = request.args.get('status_change_date')

    if record_id:
        query = query.filter(Info_Service.id == record_id)
    if service_id:
        query = query.filter(Info_Service.service_id == service_id)
    if status:
        query = query.filter(Info_Service.status == status)
    if status_change_date:
        query = query.filter(cast(Info_Service.status_change_date, String).like(f"%{status_change_date}%"))

    services_status = query.all()

    return jsonify([service_status.to_dict() for service_status in services_status]), 200
