class Customer:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.surname = data['surname']
        self.photo_url = data.get('photo_url', None)
        self.created_by = data['created_by']
        self.created_at = data['created_at']
        self.last_modify_by = data['last_modify_by']
        self.modified_at = data['modified_at']

    def __str__(self):
        template = dict(
            id = self.id,
            name = self.name,
            surname = self.surname,
            photo_url = self.photo_url,
            created_by = self.created_by,
            created_at = self.created_at,
            last_modify_by = self.last_modify_by,
            modify_at = self.modify_at,
        )
        return template