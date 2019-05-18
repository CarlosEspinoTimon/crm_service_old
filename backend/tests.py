#!/usr/bin/env python
# coding=utf-8

import unittest
from unittest import mock
import json

from server import create_app

import requests


# def mocked_requests_get(*args, **kwargs):
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code

#         def json(self):
#             return self.json_data
    
#     url = 'https://www.googleapis.com/plus/v1/people/me?access_token={}'
#     if args[0] == url.format('good_token'):
#         return MockResponse({"emails": [
#                                 {"value": "admin@email.com",
#                                 "type": "account"}]
#                             }, 200)
#     elif args[0] == url.format('forbidden_token'):
#         return MockResponse({"emails": [
#                                 {"value": "another@email.com",
#                                 "type": "account"}]
#                             }, 200)    
#     elif args[0] == url.format('wrong_token'):
#         return MockResponse({"code": 401,
#                             "message": "Invalid Credentials"
#                             }, 401)
#     elif args[0] == url.format('user_2_token'):
#         return MockResponse({"emails": [
#                                 {"value": "user@email.com",
#                                 "type": "account"}]
#                             }, 200)
#     elif arg[0] != '':
#         res = resquests.get(args[0])
#         data = json.loads(res.get_data(as_text=True))
#         return MockResponse(data, res.status_code)

#     return MockResponse(None, 404)

class BasicTestCase(unittest.TestCase):
    "Test Class"


    def setUp(self):
        '''
        Setup function
        '''
        self.app = create_app('config.Test')
        self.tester_app = self.app.test_client()
        self.token = 'eyJ0eXAiOiJKV0QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTU4MTM4OTc1LjQwNTM3M30.vqqyMyntbh2D5O7-_9tTTuLqfhtBCnTX49T6kB7nA28'

    
    def create_customer(self, name, surname):
        '''
        Function that given a customer id it creates the customer mocking the
        call to check the token.
        :param str name: the customer name
        :param str surname: the customer surname
        '''
        
        return self.tester_app.post('/customer',
                                data=json.dumps(dict(
                                    name=name,
                                    surname=surname
                                )),
                                content_type='application/json',
                                headers={'access_token': 'good_token'})


    def create_user(self, email):
        '''
        Function that creates the customer mocking the call to check the token.
        :param str email: the customer email
        '''
        
        return self.tester_app.post('/admin/user',
                                data=json.dumps(dict(
                                    email=email
                                )),
                                content_type='application/json',
                                headers={'access_token': 'good_token'})


    def delete_customer(self, customer):
        '''
        Function that given a customer id it deletes the customer mocking the
        call to check the token.
        :param int customer: the customer id
        '''
        res = self.tester_app.delete('/customer/{}'.format(customer),
                                        headers={'access_token': 'good_token'}) 


    def delete_user(self, user):
        '''
        Function that given a user id it deletes the user mocking the
        call to check the token.
        :param int user: the user id
        '''
        res = self.tester_app.delete('/admin/user/{}'.format(user),
                                        headers={'access_token': 'good_token'}) 


    def clean_dict(self, received_dict):
        '''
        Function that cleans the received data to be compared before the
        assertion.
        '''
        to_pop = ['id', 'created_at', 'modified_at']
        
        for e in to_pop:
            received_dict.pop(e)
        
    
    def test_server_running(self):
        '''
        Check if the server is running.
        '''
        res = self.tester_app.get('/')
                                
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data, 'The server is running!!')


    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_forbidden_access(self, mock_get):
    #     '''
    #     Check when a user has a valid token but it has forbidden access.
    #     '''
        
    #     res = self.tester_app.get('/customers/',
    #                             headers={'access_token': 'forbidden_token'})
    #     self.assertEqual(res.status_code, 403)
    #     data = json.loads(res.get_data(as_text=True))
    #     self.assertEqual(data, 'Forbidden')       


    def test_invalid_token(self):
        '''
        Check when the user has invalid  token .
        '''
        from functools import wraps

        def mock_decorator(*args, **kwargs):
            def check_token(func):
                @wraps(func)
                def decorated_funcion(*args, **kwargs):
                    return func(*args, **kwargs)
                return decorated_funcion
            return decorator
        res = self.tester_app.get('/customers/',
                                headers={'username': self.token})
        self.assertEqual(res.status_code, 401)
        # data = json.loads(res.get_data(as_text=True))
        # self.assertEqual(data, 'Signature verification failed')    

    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_get_customers_list_empty(self, mock_get):
    #     '''
    #     Check the list with no customers.
    #     '''
    #     res = self.tester_app.get('/customers/',
    #                             headers={'access_token': 'good_token'})
    #     self.assertEqual(res.status_code, 200)
    #     data = json.loads(res.get_data(as_text=True))
    #     self.assertEqual(data, [])     


    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_create_customer(self, mock_get):
    #     '''
    #     Creates a user, check is inserted and deleted.
    #     '''
    #     res = self.create_customer('name', 'surname')

    #     self.assertEqual(res.status_code, 201)
    #     data = json.loads(res.get_data(as_text=True))
        
    #     created = data['id']
    #     self.clean_dict(data)
            
    #     expect_res = dict(eval('''{'created_by': 1, 
    #             'last_modify_by': 1, 
    #             'name': 'name', 
    #             'photo_url': None, 
    #             'surname': 'surname'}'''))
        
    #     self.assertDictEqual(data, expect_res)   

    #     self.delete_customer(created) 


    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_list_with_two_customers(self, mock_get):
    #     '''
    #     Creates a user, check is inserted and deleted.
    #     '''
    #     res = self.create_customer('name', 'surname')
    #     data = json.loads(res.get_data(as_text=True))
    #     created = [data['id']]
    #     res = self.create_customer('name2', 'surname2')
    #     data = json.loads(res.get_data(as_text=True))
    #     created.append(data['id'])
    #     self.assertEqual(res.status_code, 201)
        
    #     self.clean_dict(data)
            
    #     expect_res = [dict(eval('''{'created_by': 1, 
    #             'last_modify_by': 1, 
    #             'name': 'name', 
    #             'photo_url': None, 
    #             'surname': 'surname'}'''))]
    #     expect_res.append(dict(eval('''{'created_by': 1, 
    #             'last_modify_by': 1, 
    #             'name': 'name2', 
    #             'photo_url': None, 
    #             'surname': 'surname2'}''')))
        
    #     res = self.tester_app.get('/customers/',
    #                             headers={'access_token': 'good_token'})
    #     self.assertEqual(res.status_code, 200)
    #     data = json.loads(res.get_data(as_text=True))
    #     self.assertTrue(len(data) == 2)

    #     for customer in data:
    #         self.clean_dict(customer)
        
    #     self.assertListEqual(data, expect_res)     
    #     for customer in created:
    #         self.delete_customer(customer) 

    
    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_get_users_just_with_admin_user(self, mock_get):
    #     '''
    #     Check the list with just the admin user.
    #     '''
    #     res = self.tester_app.get('/admin/users/',
    #                             headers={'access_token': 'good_token'})
    #     self.assertEqual(res.status_code, 200)
    #     data = json.loads(res.get_data(as_text=True))
    #     self.assertTrue(len(data) == 1)     


    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_create_user(self, mock_get):
    #     '''
    #     Creates a user, check is inserted and deleted.
    #     '''
    #     res = self.create_user('user@email.com')

    #     self.assertEqual(res.status_code, 201)
    #     data = json.loads(res.get_data(as_text=True))
        
    #     created = data['id']
    #     self.clean_dict(data)
            
    #     expect_res = dict(eval('''{'admin': 0, 
    #                     'admin_privileges_by': None, 
    #                     'created_by': 1, 
    #                     'email': 'user@email.com', 
    #                     'modified_by': 1}'''))

                
    #     self.assertDictEqual(data, expect_res)   
    #     self.delete_user(created) 

    
    

    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    # def test_update_customer(self, mock_get):
    #     '''
    #     Creates a customer, then a user and updates the customer with the new
    #     user it and check the updated id
    #     '''
    #     res = self.create_user('user@email.com')
    #     data = json.loads(res.get_data(as_text=True))
    #     user = data['id']

    #     res = self.create_customer('name', 'surname')
    #     data = json.loads(res.get_data(as_text=True))
    #     customer = data['id']
    #     self.clean_dict(data)
            
    #     expect_res = dict(eval('''{'created_by': 1, 
    #             'last_modify_by': 1, 
    #             'name': 'name', 
    #             'photo_url': None, 
    #             'surname': 'surname'}'''))
        
    #     self.assertDictEqual(data, expect_res)  
    #     res = self.tester_app.put('/customer/{}'.format(customer),
    #                             data=json.dumps(dict(
    #                                 name='name2',
    #                                 surname='surname2'
    #                             )),
    #                             content_type='application/json',
    #                             headers={'access_token': 'user_2_token'})
    #     self.assertEqual(res.status_code, 200)
        
    #     res = self.tester_app.get('/customer/{}'.format(customer),
    #                             headers={'access_token': 'user_2_token'})
        
    #     data = json.loads(res.get_data(as_text=True))
    #     self.clean_dict(data)
        
    #     expect_res = dict(eval('''{'created_by': 1, 
    #             'name': 'name2', 
    #             'photo_url': None, 
    #             'surname': 'surname2'}'''))
    #     expect_res['last_modify_by'] = user
                
    #     self.assertDictEqual(data, expect_res)   
    #     self.delete_customer(customer)
    #     self.delete_user(user)


if __name__ == '__main__':
    unittest.main()