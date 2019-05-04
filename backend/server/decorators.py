from functools import wraps
from flask import jsonify, request
from sqlalchemy import and_

from .helpers.db_helper import get_table



def check_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        import requests
        try:
            token = request.headers.get('access_token')
            if not token:
                return jsonify('Unauthorized, you must log in'), 401
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
                    return jsonify('Forbidden'), 403
            elif res.status_code == 401:
                return jsonify('''Invalid credentials or token expired'''), 401                        
            
            return jsonify('Unauthorized'), 401
        except Exception as e:
            pass
            print("Error, ", e)
            return jsonify('Error'), 500
    return decorated_funcion


def check_admin(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        import requests
        try:
            token = request.headers.get('access_token')
            if not token:
                return jsonify('Unauthorized, you must log in'), 401
            url = 'https://www.googleapis.com/plus/v1/people/me?access_token='
            res = requests.get(url+token)
            if res.status_code == 200:
                email = res.json()['emails'][0]['value']
                user_table = get_table('users')
                user = user_table.select(and_(
                                    user_table.c.email == email,
                                    user_table.c.admin == 1,
                                )).execute().first()
                if user:
                    return func(*args, **kwargs)
                else:    
                    return jsonify('Forbidden, you are not an admin'), 403
            elif res.status_code == 401:
                return jsonify('''Invalid credentials or token expired'''), 401                        
            
            return jsonify('Unauthorized'), 401
        except Exception as e:
            pass
            print("Error, ", e)
            return jsonify('Error'), 500
    return decorated_funcion