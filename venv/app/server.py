# Purpose: create a basic REST interface that can store and retrieve people information
#
# To start app, from the same directory as this file, run from the command line:
#   FLASK_APP=server.py FLASK_ENV=development flask run

from flask import Flask, request, json
from flask_restful import Resource, Api
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///rest_api.db')
app = Flask(__name__)
api = Api(app)

class People(Resource):
  def get(self, person_id):
    try:
      conn = db_connect.connect()
      query = conn.execute("SELECT * FROM people WHERE id = %s" %str(person_id))
      person_list = query.cursor.fetchall()[0]
      return json.jsonify(id=person_list[0],
                          name=person_list[1],
                          age=person_list[2],
                          locale=person_list[3])
    except Exception:
      return "Encountered an error. Are you sure the person ID you requested exists?"

  def delete(self, person_id):
    try:
      conn = db_connect.connect()
      query = conn.execute("DELETE FROM people WHERE id = %s;" %str(person_id))
    except Exception:
      return "Failed to delete person with ID %s, are you sure this ID exists?" %str(person_id)

  # Note: using PUT instead of POST here. This is because each class can only have 1 associated route.
  #  I chose to have all 3 actions (get/delete/put) in 1 class because that is clearer to me.
  def put(self, person_id):
    try:
      conn = db_connect.connect()
      new_person_dict = json.loads(request.form['data'])
      query = conn.execute("INSERT INTO people (id, name, age, locale) \
                            VALUES ('{}', '{}', {}, '{}');".format(new_person_dict['id'], new_person_dict['name'], new_person_dict['age'], new_person_dict['locale']) )
      return "Successfully created person with ID {}".format(new_person_dict['id'])
    except Exception:
      return "Failed to create person with ID {}".format(str(new_person_dict['id']))

api.add_resource(People, '/resources/data/<string:person_id>')
