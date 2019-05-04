from flask import current_app, abort

from sqlalchemy import Table, desc, and_

from server.helpers.db_helper import get_table, get_session
from server.models.user import User

import requests

from datetime import datetime

from werkzeug import exceptions


def get_user_by_id(id):
    '''
    Function that given an id it returns the user
    :param int id: the user's id
    :return cutomer: The User
    :rtype: User
    '''
    user_table = get_table('users')
    res = user_table.select(user_table.c.id == id).execute().first()
    return User({k:v for k,v in res.items()})

def create_user(sess, data, admin_id):
    '''
    Function that given the user info it creates a new user in the
    database.
    :param Session sess: The session of the connection with the database.
    :param dict data: A dictonary with the minimum user data needed.
    :param int user_id: The id of the user that is creating the user.
    :return user: The User created.
    :rtype: User.
    '''

    user_table = get_table('users')
    stmt = user_table.insert().values(
        email = data['email'],
        admin = False,
        admin_privileges_by = None,
        created_at = datetime.now(),
        modified_at = datetime.now(),
        created_by = admin_id,
        modified_by = admin_id,
    )

    sess.execute(stmt)
    stmt = user_table.select().order_by(desc(user_table.c.id))

    return User({k:v for k,v in sess.execute(stmt).first().items()})

    
def update_user(sess, user_id, data, admin_id):
    '''
    Function that given the user info it updates it.
    :param Session sess: The session of the connection with the database.
    :param int user_id: The id of the user that is been updated.
    :param dict data: A dictonary with the minimum user data needed.
    :param int user_id: The id of the user that is updating the user.
    '''

    user_table = get_table('users')
    stmt = user_table.update().values(
        email = data['email'],
        modified_at = datetime.now(),
        modified_by = admin_id
    ).where(user_table.c.id == user_id)
    
    res = sess.execute(stmt)
    if res.rowcount == 0:
        raise Exception("User not found")
    

def delete_user_by_id(sess, user_id):
    '''
    Function that given the user id it deletes it.
    :param Session sess: The session of the connection with the database.
    :param int user_id: The id of the user that is been deleted.
    '''
    user_table = get_table('users')
    stmt = user_table.delete().where(user_table.c.id == user_id)

    res = sess.execute(stmt)
    if res.rowcount == 0:
        raise Exception("User does not exists")
    
  

def get_admin_id(token):
    '''
    Function that given a token, it returns its user id if the user has admin
    privileges.
    :param srt token: the token.
    :return: the id of the user.
    :rtype: int
    '''
    try:
        url = 'https://www.googleapis.com/plus/v1/people/me?access_token='
        res = requests.get(url+token)
        if res.status_code == 200:
            email = res.json()['emails'][0]['value']
            user_table = get_table('users')
            user = user_table.select().where(and_(
                            user_table.c.email == email,
                            user_table.c.admin == 1
                            )).execute().first()
            if user:
                return user['id']
            else:
                abort(403)
        abort(401)
    except Exception as e:
        if type(e) == exceptions.Unauthorized:
            abort(401, 'User not found or not enough privileges')
        elif type(e) == exceptions.Forbidden:
            abort(403, 'You not an admin')
        abort(500, 'Server error')

def update_user_status(sess, user_id, data, admin_id):
    '''
    Function that given a user's id and an admin_id, it changes the status of
    the user, granting or revoquin it's admin privileges.
    :param Session sess: The session of the connection with the database.
    :param int user_id: The id of the user that is been updated.
    :param dict data: The data us the user to change it's status.
    :param int admin_id: The id of the admin that is executing the action.
    '''
    user_table = get_table('users')
    stmt = user_table.update().where(
            user_table.c.id == user_id
        ).values(
            admin = data['admin'],
            admin_privileges_by = admin_id,
            modified_at = datetime.now(),
            modified_by = admin_id
        )

    res = sess.execute(stmt)
    if res.rowcount == 0:
        raise Exception("User not found")


