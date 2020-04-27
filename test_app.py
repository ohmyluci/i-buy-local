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
        self.database_name = "i_buy_local"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','EresTonto','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
        res = self.client().get('/customers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_businesses_bad_token(self):
        auth_header = { 'Authorization': 'Bearer EyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5OTdQNGFTeHFSMEpOVTBQNXdJTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1paTI0ci05cy5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTU1OTg0Njc2NTY1MTUzMjQ2NzkiLCJhdWQiOlsiaS1idXktbG9jYWwiLCJodHRwczovL2Rldi1paTI0ci05cy5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg4MDAxMTk2LCJleHAiOjE1ODgwODc1OTYsImF6cCI6IkpuSnF5T2QxYW9NcFZ5Zzh2QzdaQmxHQ2VBMUJqMDMwIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpidXNpbmVzcy1kZXRhaWwiXX0.kB0EOVUq6IpiX-ytq1j6Q8Oou78gvpEPD7dKprPWsr6BwdaRhubbkqPSC-lsYEsg4FnDLWIRnAUvHZoCvD0kbFUlIXABt3dYyFH9cF5nDVXWqTrc8oj32Pd2f5t0tuffLGvDs4wnXos4mTPT2v8s91teh75kiEY_orZZXccnNvl-wqk9sLK5a47wV5aaqqaYP7PboE8V2sA0LofhE-LebMPamYWERA0eYYkqTwRXJVfxDLNfqpKOpk0CZZoHI6pLlMWkZ-DnlMmFoaa1ZETwMtuC-h9pBiY0G6XvB0OwBJ2h8ae7h7QdEckR8jzMf2qIvQvVGap1d2_gUUU7XRsPYQ'}
        res = self.client().get('/businesses/1', headers=auth_header)

        self.assertEqual(res.status_code, 400)


    def test_get_businesses_good_token(self):
        auth_header = { 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5OTdQNGFTeHFSMEpOVTBQNXdJTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1paTI0ci05cy5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTU1OTg0Njc2NTY1MTUzMjQ2NzkiLCJhdWQiOlsiaS1idXktbG9jYWwiLCJodHRwczovL2Rldi1paTI0ci05cy5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg4MDAxMTk2LCJleHAiOjE1ODgwODc1OTYsImF6cCI6IkpuSnF5T2QxYW9NcFZ5Zzh2QzdaQmxHQ2VBMUJqMDMwIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpidXNpbmVzcy1kZXRhaWwiXX0.kB0EOVUq6IpiX-ytq1j6Q8Oou78gvpEPD7dKprPWsr6BwdaRhubbkqPSC-lsYEsg4FnDLWIRnAUvHZoCvD0kbFUlIXABt3dYyFH9cF5nDVXWqTrc8oj32Pd2f5t0tuffLGvDs4wnXos4mTPT2v8s91teh75kiEY_orZZXccnNvl-wqk9sLK5a47wV5aaqqaYP7PboE8V2sA0LofhE-LebMPamYWERA0eYYkqTwRXJVfxDLNfqpKOpk0CZZoHI6pLlMWkZ-DnlMmFoaa1ZETwMtuC-h9pBiY0G6XvB0OwBJ2h8ae7h7QdEckR8jzMf2qIvQvVGap1d2_gUUU7XRsPYQ'}
        res = self.client().get('/businesses/1', headers=auth_header)

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
if __name__ == "__main__":
    unittest.main()