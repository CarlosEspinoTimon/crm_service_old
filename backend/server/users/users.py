from flask import Blueprint, jsonify, request, abort
from flask_cors import CORS, cross_origin

from server.models.customer import Customer

from server.helpers.db_helper import get_table, get_session
from server.helpers.images import upload_image

from .helper import create_customer, update_customer, delete_customer_by_id, \
                    get_user_id, get_url_stored_image

from server.decorators import check_token



users = Blueprint('users', __name__, url_prefix='/')
CORS(users, max_age=30*86400)

@users.route('/customers', methods=['GET'])
@check_token
def get_all_customers():
    '''
    Function that returns all the customers.
    :return customers: All the customers.
    :rtype: list of Customers.
    '''
    try:
        cust_table = get_table('customers')
        res = cust_table.select().execute()
        customers = [Customer({k:v for k,v in row.items()}).__str__() \
                                    for row in res]
    except Exception as e:
        # TODO catch the error to ignore database errors
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(customers), 200


@users.route('/customer/<int:id>', methods=['GET'])
@check_token
def get_customer(id):
    '''
    Function that given an id it returns the customer.
    :param int id: the id of the customer.
    :return customer: The customer.
    :rtype: Customer.
    '''
    try:
        customer = get_customer(id)
    except Exception as e:
        # TODO catch the error to ignore database errors
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(customer.__str__()), 200


@users.route('/customer', methods=['POST'])
@check_token
def post_customer():
    '''
    Function that given the customer data it creates it.
    :param dict data: the data of the customer sent in the body of the request.
    :return customer: The customer.
    :rtype: Customer.
    '''
    sess = get_session()
    try:
        user_id = get_user_id(request.headers.get('access_token'))
        data = request.get_json()
        if data.get('photo'):
            image = data['photo'].get('str_image')
            extension = data['photo'].get('extension')
            content_type = 'image/{}'.format(extension[1:])
            data['photo_url'] = upload_image(image, content_type, extension)
        customer = create_customer(sess, data, user_id)
        sess.commit()
    except Exception as e:
        # TODO catch the error to ignore database errors
        sess.rollback()
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(customer.__str__()), 201


@users.route('/customer/<int:customer_id>', methods=['PUT'])
@check_token
def put_customer(customer_id):
    '''
    Function that given the customer data and its customer_id it updates it.
    :param int customer_id: the id of the customer.
    :param dict data: the data of the customer sent in the body of the request.
    '''
    sess = get_session()
    try:
        user_id = get_user_id(request.headers.get('access_token'))
        data = request.get_json()
        if data.get('photo'):
            image = data['photo'].get('str_image')
            extension = data['photo'].get('extension')
            content_type = 'image/{}'.format(extension[1:])
            url = get_url_stored_image(customer_id)
            data['photo_url'] = upload_image(image, content_type, extension, 
                                            url)
        update_customer(sess, customer_id, data, user_id)
        sess.commit()
    except Exception as e:
        # TODO catch the error to ignore database errors
        sess.rollback()
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify('Customer updated'), 200


@users.route('/customer/<int:id>', methods=['DELETE'])
@check_token
def delete_customer(id):
    '''
    Function that given the customer id it deletes it.
    :param int id: the id of the customer.
    '''
    try:
        sess = get_session()
        delete_customer_by_id(sess, id)
        sess.commit()
    except Exception as e:
        # TODO catch the error to ignore database errors
        sess.rollback()
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify('Customer deleted'), 200
    

