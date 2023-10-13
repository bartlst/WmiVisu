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
    ip_address = db.Column(db.String(15), unique=True)
    connection_status = db.Column(db.Integer, unique=True)


class Spec_OS(db.Model):
    __tablename__ = 'spec_os'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    os_name_version = db.Column(db.String(255), nullable=False)
    architecture = db.Column(db.String(10), nullable=False)
    license_key = db.Column(db.String(255))
    activation_status = db.Column(db.String(50))
    install_date = db.Column(db.DateTime, nullable=False)
    last_boot_up_time = db.Column(db.DateTime, nullable=False)


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


class Spec_NetworkInterface(db.Model):
    __tablename__ = 'spec_networkinterface'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    interface_name = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50))
    subnet_mask = db.Column(db.String(50))
    gateway = db.Column(db.String(50))
    mac_address = db.Column(db.String(50), nullable=False)
    link_speed = db.Column(db.String(50))


class Spec_Disk(db.Model):
    __tablename__ = 'spec_disk'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    disk_interface = db.Column(db.String(50), nullable=False)
    disk_type = db.Column(db.String(50), nullable=False)
    raid_configuration = db.Column(db.String(255))


class Spec_WatchedServices(db.Model):
    __tablename__ = 'spec_watchedservices'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


class Info_Measurements(db.Model):
    __tablename__ = 'info_measurements'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    measurement_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    cpu_usage_pct = db.Column(db.Float)
    ram_used_mb = db.Column(db.Integer)
    ram_available_mb = db.Column(db.Integer)
    network_sent_mb = db.Column(db.Integer)
    network_received_mb = db.Column(db.Integer)


class Info_DiskMeasurements(db.Model):
    __tablename__ = 'info_diskmeasurements'

    id = db.Column(db.Integer, primary_key=True)
    disk_id = db.Column(db.Integer, db.ForeignKey('spec_disk.id'), nullable=False)
    used_mb = db.Column(db.Integer, nullable=False)
    available_mb = db.Column(db.Integer, nullable=False)


class Info_ServiceStatuses(db.Model):
    __tablename__ = 'info_servicestatuses'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('spec_watchedservices.id'), nullable=False)
    status = db.Column(db.String(255), nullable=False)