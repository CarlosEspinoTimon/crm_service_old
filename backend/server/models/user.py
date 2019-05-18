from datetime import datetime
from time import time
from server import db
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Integer, index=True)
    admin_privileges_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '< {}>'.format(self.username)
    
    def __str__(self):
        template = dict(
            id = self.id,
            email = self.email,
            admin = self.admin,
            admin_privileges_by = self.admin_privileges_by,
            created_at = self.created_at,
            modified_at = self.modified_at,
            modified_by = self.modified_by,
            created_by = self.created_by
        )
        return template


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_auth_token(self, expiration=300):
        return jwt.encode({
                    'id': self.id,
                    'exp': time() + expiration
                }, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')