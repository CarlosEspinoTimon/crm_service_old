from flask import current_app

from sqlalchemy import Table, desc

from server.helpers.db_helper import get_table, get_session
from server.models.customer import Customer

import requests


def get_customer(id):
    '''
    Function that given an id it returns the customer
    :param int id: the customer's id
    :return cutomer: The Customer
    :rtype: Customer
    '''
    cust_table = get_table('customers')
    res = cust_table.select(cust_table.c.id == id).execute().first()
    return Customer({k:v for k,v in res.items()})

def create_customer(sess, data, user_id):
    '''
    Function that given the customer info it creates a new customer in the
    database.
    :param Session sess: The session of the connection with the database.
    :param dict data: A dictonary with the minimum customer data needed.
    :param int user_id: The id of the user that is creating the customer.
    :return customer: The Customer created.
    :rtype: Customer.
    '''

    cust_table = get_table('customers')
    stmt = cust_table.insert().values(
        name = data['name'],
        surname = data['surname'],
        photo_url = data.get('photo_url'),
        created_by = user_id,
        last_modify_by = user_id
    )

    sess.execute(stmt)
    stmt = cust_table.select().order_by(desc(cust_table.c.id))

    return Customer({k:v for k,v in sess.execute(stmt).first().items()})

    
def update_customer(sess, customer_id, data, user_id):
    '''
    Function that given the customer info it updates it.
    :param Session sess: The session of the connection with the database.
    :param int customer_id: The id of the customer that is been updated.
    :param dict data: A dictonary with the minimum customer data needed.
    :param int user_id: The id of the user that is updating the customer.
    '''

    cust_table = get_table('customers')
    stmt = cust_table.update().values(
        name = data['name'],
        surname = data['surname'],
        photo_url = data.get('photo_url'),
        last_modify_by = user_id
    ).where(cust_table.c.id == customer_id)
    
    res = sess.execute(stmt)
    if res.rowcount == 0:
        raise Exception("User not found")
    

def delete_customer_by_id(sess, customer_id):
    '''
    Function that given the customer id it deletes it.
    :param Session sess: The session of the connection with the database.
    :param int customer_id: The id of the customer that is been deleted.
    '''
    try:
        cust_table = get_table('customers')
        stmt = cust_table.delete().where(cust_table.c.id == customer_id)

        sess.execute(stmt)
    except Exception:
        print("EEEE")

def get_user_id(token):
    '''
    Function that given a token, it returns its user id.
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
            user = user_table.select(
                            user_table.c.email == email).execute().first()
            if user:
                return user['id']
        raise Exception('User not found', 500)
    except Exception as e:
        pass
        print("Error: ", e)
        raise Exception('Server error', 500)

def get_url_stored_image(customer_id):
    '''
    Function that given a customer_id returns the url of its image.
    :param int customer_id: the id of the customer.
    :return: the url of the image.
    :rtype: string
    '''
    cust_table = get_table('customers')
    res = cust_table.select(cust_table.c.id == customer_id).execute().first()
    return res['photo_url'] if res else []
    
    


