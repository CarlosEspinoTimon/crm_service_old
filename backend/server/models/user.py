from flask_login import  UserMixin
class User(UserMixin):
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.admin = data['admin']
        self.admin_privileges_by = data['admin_privileges_by']
        self.access_token = data.get('access_token', None)

    def __str__(self):
        template = dict(
            id = self.id,
            email = self.email,
            admin = self.admin,
            photo_url = self.photo_url,
            admin_privileges_by = self.admin_privileges_by,
            access_token = self.access_token
        )
        return template

    def get_id(self):
        return self.id
    


# from flask_login import  UserMixin


# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), nullable=False)
#     admin = db.Column(db.Boolean, nullable=False)
#     admin_privileges_by = db.Column(db.Integer, nullable=False)