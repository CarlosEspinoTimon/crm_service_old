from datetime import datetime
from server import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    surname = db.Column(db.String(120), index=True)
    photo_url = db.Column(db.String(120), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '< {}>'.format(self.username)
    
    def __str__(self):
        template = dict(
            id = self.id,
            name = self.name,
            surname = self.surname,
            photo_url = self.photo_url,
            created_by = self.created_by,
            last_modified_by = self.last_modified_by,
            created_at = self.created_at,
            last_modified_at = self.last_modified_at,
        )
        return template

