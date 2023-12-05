import secrets
from . import db
from flask_login import UserMixin
from sqlalchemy import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(24), nullable=False)
    api_key = db.Column(db.String(48), unique=True)
    reset_password = db.Column(db.Boolean, nullable=False)

    def generate_api_key(self):
        self.api_key = secrets.token_urlsafe(48)

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    cause_type = db.Column(db.String(48), nullable=False)
    resolved = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'server_id': self.server_id,
            'cause_type': self.cause_type,
            'resolved': self.resolved,
            'date': self.date
        }

class Servers(db.Model):
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(128), unique=True)
    connection_status = db.Column(db.Integer)
    remove = db.Column(db.Integer)

    services = db.relationship('Spec_Service', backref='server', cascade="all, delete-orphan")

    specification = db.relationship('Specification', backref='server', cascade="all, delete-orphan")
    disks_measurements = db.relationship('Info_DiskMeasurements', backref='server', cascade="all, delete-orphan")
    measurements = db.relationship('Info_Measurements', backref='server', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'connection_status': self.connection_status
        }

class Info_Measurements(db.Model):
    __tablename__ = 'info_measurements'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    measurement_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    cpu_usage_pct = db.Column(db.Float)
    ram_used_pct = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'measurement_date': self.measurement_date,
            'cpu_usage_pct': self.cpu_usage_pct,
            'ram_used_pct': self.ram_used_pct
        }


class Info_DiskMeasurements(db.Model):
    __tablename__ = 'info_diskmeasurements'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    measurement_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    disk_id = db.Column(db.String(4), nullable=False)
    total_space = db.Column(db.Integer, nullable=False)
    free_space = db.Column(db.Integer, nullable=False)
    used_space = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'measurement_date': self.measurement_date,
            'disk_id': self.disk_id,
            'total_space': self.total_space,
            'free_space': self.free_space,
            'used_space': self.used_space
        }

class Spec_Service(db.Model):
    __tablename__ = 'spec_services'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    watched = db.Column(db.Integer)

    info = db.relationship('Info_Service', backref='spec_services', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'watched': self.watched
        }

class Info_Service(db.Model):
    __tablename__ = 'info_services'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('spec_services.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    status_change_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'status': self.status,
            'status_change_date': self.status_change_date
        }

class Specification(db.Model):
    __tablename__ = 'specification'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)

    os = db.Column(db.String(512), nullable=False)
    motherboard = db.Column(db.String(512), nullable=False)
    cpu = db.Column(db.String(512), nullable=False)
    ram = db.Column(db.String(512), nullable=False)
    gpu = db.Column(db.String(512), nullable=False)
    disk = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'os': self.os,
            'motherboard': self.motherboard,
            'cpu': self.cpu,
            'ram': self.ram,
            'gpu': self.gpu,
            'disk': self.disk,
        }



