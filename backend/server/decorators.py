from functools import wraps
from flask import jsonify, request

from .helpers.db_helper import get_table



def check_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        import requests
        try:
            token = request.headers.get('access_token')
            url = 'https://www.googleapis.com/plus/v1/people/me?access_token='
            res = requests.get(url+token)
            if res.status_code == 200:
                email = res.json()['emails'][0]['value']
                user_table = get_table('users')
                user = user_table.select(
                                user_table.c.email == email).execute().first()
                if user:
                    return func(*args, **kwargs)
                else:    
                    return jsonify('Unauthorized'), 401
            return jsonify('Unauthorized'), 401
        except Exception as e:
            pass
            return jsonify('Error'), 500
    return decorated_funcion