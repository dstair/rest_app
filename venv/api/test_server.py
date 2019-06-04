import os
import unittest
import db
from server import app
from requests import put, get, delete
import subprocess

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
  
    def tearDown(self):
        pass

    def test_add_person_succeeds(self):
        # Note: the right way to do this is to use the put() command in Python. But the put() 
        #  command is not working, while the equivalent cURL command is. So I am implementing a hack.
        #response = self.app.put('/resources/data/', 'data={ "name": "peter", "locale": "NYC", "age": 42}')
        response = os.system('curl http://localhost:5000/resources/data/ -d\
         \'data={ "name": "peter", "locale": "NYC", "age": 42}\' -X PUT -v')
        self.assertEqual(response, 1792)

    def test_get_person_exists(self):
        # add a person so there is a person in the system
        os.system('curl http://localhost:5000/resources/data/ -d\
         \'data={ "name": "peter", "locale": "NYC", "age": 42}\' -X PUT -v')
        response = self.app.get('/resources/data/1')
        self.assertEqual(str(response.json), "{'age': 42, 'id': 1, 'locale': 'NYC', 'name': 'peter'}")
        self.assertEqual(response.status_code, 200)

    def test_get_person_missing(self):
        response = self.app.get('/resources/data/9999999999')
        self.assertEqual(response.status_code, 404)

    # Note: this test will NOT work. In order for it to work, I would want to add a new resource,
    #  get that resource's ID, and delete it. But I don't have the "add resource part" working yet.
    def test_delete_person_exists(self):
        response = self.app.delete('/resources/data/00000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json), '{\n  "age": 42, \n  "id": 12382, \n  "locale": "NYC", \n  "name": "peter"\n}\n')

    def test_delete_person_missing(self):
        response = self.app.delete('/resources/data/9999999999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
