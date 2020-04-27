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

        self.new_customer = {
            'name': "customer test",
            'address': "address test",
            'email': "email@test.com",
            'phone': "phonetest" 
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get questions without indicating pagination (default=1) should return success response
    def test_200_get_customers(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.CUSTOMER_TOKEN) }
        res = self.client().get('/customers', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_businesses_bad_token(self):
        auth_header = { 'Authorization': 'Bearer badtoken' }
        res = self.client().get('/businesses/1', headers=auth_header)

        self.assertEqual(res.status_code, 400)


    def test_get_businesses_good_token(self):
        auth_header = { 'Authorization': "Bearer {}".format(self.BUSINESS_TOKEN) }
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
if __name__ == "__main__":
    unittest.main()