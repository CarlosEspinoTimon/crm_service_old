class Customer:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.surname = data['surname']
        self.photo_url = data.get('photo_url', None)
        self.created_by = data['created_by']
        self.last_modify_by = data['last_modify_by']

    def __str__(self):
        template = dict(
            id = self.id,
            name = self.name,
            surname = self.surname,
            photo_url = self.photo_url,
            created_by = self.created_by,
            last_modify_by = self.last_modify_by,
        )
        return template