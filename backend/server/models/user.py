from flask_login import  UserMixin
class User(UserMixin):
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.admin = data['admin']
        self.admin_privileges_by = data['admin_privileges_by']
        self.created_at = data['created_at']
        self.modified_at = data['modified_at']
        self.modified_by = data['modified_by']
        self.created_by = data['created_by']

    def __str__(self):
        template = dict(
            id = self.id,
            email = self.email,
            admin = self.admin,
            admin_privileges_by = self.admin_privileges_by,
            created_at = self.created_at,
            modified_at = self.modified_at,
            created_by = self.created_by
        )
        return template

    def get_id(self):
        return self.id
