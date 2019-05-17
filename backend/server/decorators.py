from functools import wraps
from flask import jsonify, request, current_app as app

from server.models.user import User

import jwt



def check_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        username = request.headers.get('username') 
        password = request.headers.get('password')
        if username and not password:
            try:
                payload = jwt.decode(username, app.config['SECRET_KEY'], 
                                                    algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify('''Token expired'''), 401
            except jwt.InvalidSignatureError:
                return jsonify('''Signature verification failed'''), 401
            return func(*args, **kwargs)
        else:
            user = User.query.filter_by(email=username).first()
            if user and user.check_password(password):
                return func(*args, **kwargs)
            else:
                return jsonify('Forbidden'), 403

    return decorated_funcion


def check_admin(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        username = request.headers.get('username') 
        password = request.headers.get('password')
        if username and not password:
            try:
                payload = jwt.decode(username, app.config['SECRET_KEY'], 
                                                    algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify('''Token expired'''), 401
            except jwt.InvalidSignatureError:
                return jsonify('''Signature verification failed'''), 401
            user = User.query.get(payload['id'])
            if user.admin:
                return func(*args, **kwargs)
            else:
                return jsonify('Forbidden'), 403
        else:
            user = User.query.filter_by(email=username).first()
            if user and user.check_password(password):
                return func(*args, **kwargs)
            else:
                return jsonify('Forbidden'), 403

    return decorated_funcion

