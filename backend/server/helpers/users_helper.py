import jwt
from flask import current_app as app


def get_admin_id(token):
    '''
    Function that given a token, it returns its id.
    :param srt token: the token.
    :rtype: int
    ''' 
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], 
                                            algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify('''Token expired'''), 401
    except jwt.InvalidSignatureError:
        return jsonify('''Signature verification failed'''), 401
    return payload['id']
    
    
    