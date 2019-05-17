from flask import Blueprint, jsonify, request, abort
from flask_cors import CORS, cross_origin

from server.models.customer import Customer

from server.helpers.images import upload_image
from server.helpers.users_helper import get_admin_id

from datetime import datetime

from server.decorators import check_token

from werkzeug import exceptions

from server import db



controlled_exceptions = exceptions.InternalServerError, \
    exceptions.Unauthorized, exceptions.Forbidden 

users = Blueprint('users', __name__, url_prefix='/')
CORS(users, max_age=30*86400)

@users.route('/customers/', methods=['GET'])
@check_token
def get_all_customers():
    '''
    Function that returns all the customers.
    :return customers: All the customers.
    :rtype: list of Customers.
    '''
    customers = [c.__str__() for c in Customer.query.all()]
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
    customer = Customer.query.get(id)
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
    data = request.get_json()
    photo_url = None
    if data.get('photo'):
            image = data['photo'].get('str_image')
            extension = data['photo'].get('extension')
            content_type = 'image/{}'.format(extension[1:])
            photo_url = upload_image(image, content_type, extension)
    user_id = get_admin_id(request.headers.get('username'))
    customer = Customer(
        name = data.get('name'),
        surname = data.get('surname'),
        photo_url = photo_url,
        created_by = user_id,
        last_modified_by = user_id,
        created_at = datetime.now(),
        last_modified_at = datetime.now()
    )
    db.session.add(customer)
    db.session.commit()

    return jsonify(customer.__str__()), 201



@users.route('/customer/<int:customer_id>', methods=['PUT'])
@check_token
def put_customer(customer_id):
    '''
    Function that given the customer data and its customer_id it updates it.
    :param int customer_id: the id of the customer.
    :param dict data: the data of the customer sent in the body of the request.
    '''
    data = request.get_json()
    photo_url = ''
    if data.get('photo'):
            image = data['photo'].get('str_image')
            extension = data['photo'].get('extension')
            content_type = 'image/{}'.format(extension[1:])
            photo_url = upload_image(image, content_type, extension)
    user_id = get_admin_id(request.headers.get('username'))
    customer = Customer.query.get(customer_id)
    if data.get('name'): customer.name = data['name']
    if data.get('surname'): customer.surname = data['surname']
    if photo_url: customer.photo_url = photo_url
    customer.last_modified_by = user_id
    customer.last_modified_at = datetime.now()
    db.session.add(customer)
    db.session.commit()

    return jsonify('Customer updated'), 200


@users.route('/customer/<int:id>', methods=['DELETE'])
@check_token
def delete_customer(id):
    '''
    Function that given the customer id it deletes it.
    :param int id: the id of the customer.
    '''
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify('Customer deleted'), 200
    

