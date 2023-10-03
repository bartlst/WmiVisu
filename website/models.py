from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(24), nullable=False)
    reset_password = db.Column(db.Boolean, nullable=False)
    opportunity_applications = db.relationship('OpportunityApplications', cascade="all, delete-orphan")