import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class IBuyLocalTestCase(unittest.TestCase):
    """This class represents the i buy local test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "i_buy_local"
        #self.database_path = "postgres://{}:{}@{}/{}".format('postgres','EresTonto','localhost:5432', self.database_name)
        #setup_db(self.app, self.database_path)
        setup_db(self.app)

        self.BUSINESS_TOKEN = os.environ.get('BUSINESS_TOKEN')
        self.CUSTOMER_TOKEN = os.environ.get('CUSTOMER_TOKEN')

        unittest.TestLoader.sortTestMethodsUsing = None

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    
    # posting a business using a business role should create the business and return 200
    def test_post_business_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().post('/businesses', headers=auth_header, json={'id':'10',
         'name': 'business10', 'address': 'address10', 'phone':'phone10', 'cif':'cif10',
         'email':'business10@business10.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # posting a business using customer role should return 403 forbidden
    def test_post_business_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().post('/businesses', headers=auth_header, json={'id':'10',
         'name': 'business10', 'address': 'address10', 'phone':'phone10', 'cif':'cif10',
         'email':'business10@business10.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # Get business details using a business token return 200 status
    def test_get_business_detail_using_good_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Get business details using a customer token return 403 status
    def test_get_business_detail_using_invalid_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    
    # patching a business using a business role should edit the business and return 200
    def test_patching_business_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().patch('/businesses', headers=auth_header, json={'id':'1',
         'name': 'business1_b', 'address': 'address1_b', 'phone':'phone1', 'cif':'cif1',
         'email':'business1@business1.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # patching a business using a customer role should return 403
    def test_patching_business_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().patch('/businesses', headers=auth_header, json={'id':'1',
         'name': 'business1_b', 'address': 'address1_b', 'phone':'phone1', 'cif':'cif1',
         'email':'business1@business1.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # deleting a business using business role should return 200
    def test_delete_business_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().delete('/businesses/10', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # deleting a business using customer role should return 403 forbidden
    def test_delete_business_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().delete('/businesses/10', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)



    # Get a list of businesses using a invalid token return 400 error status
    def test_get_businesses_bad_token(self):
        auth_header = { 'Authorization': 'Bearer badtoken' }
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    # Get list of businesses using a valid token return 200 status
    def test_get_businesses_good_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # Get list customers using valid customer token return a 200 status
    def test_200_get_customers_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().get('/customers', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # Get list customers using business token return a 200 status
    def test_200_get_customers_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().get('/customers', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # posting a customer using a customer role should create the customer and return 200
    def test_post_customer_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().post('/customers', headers=auth_header, json={'id':'10',
         'name': 'customer10', 'address': 'address10', 'phone':'phone10',
         'email':'customer10@customer10.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # posting a customer using business role should return 403 forbidden
    def test_post_customer_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().post('/customers', headers=auth_header, json={'id':'10',
         'name': 'customer10', 'address': 'address10', 'phone':'phone10',
         'email':'customer10@customer10.com'})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # Get customer details using a customer token return 200 status
    def test_get_customer_detail_using_good_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().get('/customers/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Get customer details using a business token return 403 status
    def test_get_customer_detail_using_invalid_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().get('/customers/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    
    # deleting a customer using customer role should return 200
    def test_delete_customer_using_business_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().delete('/customers/10', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # deleting a customer using business role should return 403 forbidden
    def test_delete_customer_using_customer_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().delete('/customers/10', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)



    # Get a list of customers using a invalid token return 400 error status
    def test_get_customers_bad_token(self):
        auth_header = { 'Authorization': 'Bearer badtoken' }
        res = self.client().get('/customers/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    # Get list of customers using a valid token return 200 status
    def test_get_customers_good_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().get('/customers/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    



    
if __name__ == "__main__":
    unittest.main()