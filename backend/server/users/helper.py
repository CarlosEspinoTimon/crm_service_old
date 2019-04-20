from flask import current_app

from sqlalchemy import Table, desc

from server.helpers.db_helper import get_table, get_session
from server.models.customer import Customer


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
        photo_url = data['photo_url'],
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
        photo_url = data['photo_url'],
        last_modify_by = user_id
    ).where(cust_table.c.id == customer_id)

    sess.execute(stmt)

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