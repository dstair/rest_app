import os
import unittest
import db
from server import app
from requests import put, get, delete

#TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
#       app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        #db.init_db()
  
    # executed after each test
    def tearDown(self):
        pass

    def test_add_person_succeeds(self):
        response = self.app.put('/resources/data/')
        self.assertEqual(response.status_code, 200)

    def test_get_person_exists(self):
        response = self.app.get('/resources/data/12382')
        #self.assertEqual(response.content, '{\n  "age": 27, \n  "id": 12383, \n  "locale": "NYC", \n  "name": "peter"\n}\n')
        self.assertEqual(response.status_code, 200)
        # TODO: add assertion that JSON object was also returned

    def test_get_person_missing(self):
        response = self.app.get('/resources/data/9999999999')
        self.assertEqual(response.status_code, 404)

    def test_delete_person_exists(self):
        response = self.app.delete('/resources/data/12381')
        self.assertEqual(response.status_code, 200)
        #TODO: add assertion that JSON object of person was returned

    def test_delete_person_missing(self):
        response = self.app.delete('/resources/data/9999999999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
