from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(24), nullable=False)
    reset_password = db.Column(db.Boolean, nullable=False)


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    cause_type = db.Column(db.String(50), nullable=False)
    cause_id = db.Column(db.Integer, nullable=False)


class Servers(db.Model):
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(128), unique=True)
    connection_status = db.Column(db.Integer)

    services = db.relationship('Spec_Service', backref='server')
    os_specs = db.relationship('Spec_OS', backref='server')
    motherboards = db.relationship('Spec_Motherboard', backref='server')
    gpus = db.relationship('Spec_GPU', backref='server')
    disks = db.relationship('Info_DiskMeasurements', backref='server')
    watched_services = db.relationship('Spec_WatchedServices', backref='server')
    measurements = db.relationship('Info_Measurements', backref='server')
    networkAdapters = db.relationship('Spec_NetworkAdapter', backref='server')

class Spec_OS(db.Model):
    __tablename__ = 'spec_os'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    os_name_version = db.Column(db.String(255), nullable=False)
    architecture = db.Column(db.String(10), nullable=False)
    install_date = db.Column(db.DateTime, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)


class Spec_Motherboard(db.Model):
    __tablename__ = 'spec_motherboard'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    bios_version = db.Column(db.String(100), nullable=False)


class Spec_GPU(db.Model):
    __tablename__ = 'spec_gpu'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    memory_size = db.Column(db.Float, nullable=False)
    driver_version = db.Column(db.String(100), nullable=False)


class Spec_WatchedServices(db.Model):
    __tablename__ = 'spec_watchedservices'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    service_statuses = db.relationship('Info_ServiceStatuses', backref='service')


class Info_Measurements(db.Model):
    __tablename__ = 'info_measurements'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    measurement_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    cpu_usage_pct = db.Column(db.Float)
    ram_used_pct = db.Column(db.Integer)


class Info_DiskMeasurements(db.Model):
    __tablename__ = 'info_diskmeasurements'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    disk_id = db.Column(db.String(3), nullable=False)
    total_space = db.Column(db.Integer, nullable=False)
    free_space = db.Column(db.Integer, nullable=False)
    used_space = db.Column(db.Integer, nullable=False)



# Network adaptery są problematyczne
class Spec_NetworkAdapter(db.Model):
    __tablename__ = 'spec_network_adapter'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mac_address = db.Column(db.String(100), nullable=True)


class NetworkAdapterUsage(db.Model):
    __tablename__ = 'network_adapter_usage'

    id = db.Column(db.Integer, primary_key=True)
    adapter_id = db.Column(db.Integer, db.ForeignKey('spec_network_adapter.id'), nullable=False)
    measurement_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    bytes_sent = db.Column(db.Integer, nullable=False)
    bytes_received = db.Column(db.Integer, nullable=False)


class Spec_Service(db.Model):
    __tablename__ = 'spec_services'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    watched = db.Column(db.Integer)


class Info_Service(db.Model):
    __tablename__ = 'info_services'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('spec_service.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    status_change_date = db.Column(db.DateTime, nullable=False)