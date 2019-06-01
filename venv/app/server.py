# Purpose: create a basic REST interface that can store and retrieve people information
#
# To start app, from the same directory as this file, run from the command line:
#   FLASK_APP=server.py FLASK_ENV=development flask run

from flask import Flask, request, json
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
#import json

db_connect = create_engine('sqlite:///rest_api.db')
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class People(Resource):
  def get(self, person_id):
    try:
      conn = db_connect.connect()
      query = conn.execute("SELECT * FROM people WHERE id = %s" %str(person_id) )
      return json.jsonify(query.cursor.fetchall())
    except Exception:
      return "Encountered an error. Are you sure the person ID you requested exists?"

  def delete(self, person_id):
    try:
      conn = db_connect.connect()
      query = conn.execute("DELETE FROM people WHERE id = %s;" %str(person_id))
    except Exception:
      return "Failed to delete person with ID %s, are you sure this ID exists?" %str(person_id)

  def post(self, person_id):
    #try:
      new_person_dict = parser.parse_args()
      return str(new_person_dict)
      conn = db_connect.connect()
      #new_person_dict = json.loads(new_person)
      query = conn.execute("INSERT INTO people (id, name, age, locale) \
                            VALUES ('{}', '{}', {}, '{}');".format(new_person_dict['id'], new_person_dict['name'], new_person_dict['age'], new_person_dict['locale']) )
    #except Exception:
    #  return "Failed to delete person with ID {}, are you sure this ID exists?".format(str(new_person_dict))



api.add_resource(People, '/resources/data/<string:person_id>')


# curl http://localhost:5000/resources/data/12345
# curl http://localhost:5000/resources/data/12346 -d '{ "id":"12346", "name":"Peter Smith", "age":30, "locale":"New York"}' -X POST -v
# curl http://localhost:5000/resources/data/12345 -X DELETE -v



#@app.route("/resources/data", methods = ["GET"])
#def put_person():
#    conn = db_connect.connect()
#    query = conn.execute("select * from people")
#    return str(query.cursor.fetchall())
#    # use request.form() to validate the data posted and write it to the database.
#
#
#@app.route("/resources/data/<string:person_id>", methods = ["GET", "DELETE"])
#def get_person(person_id):
#    conn = db_connect.connect()
#    query = conn.execute("SELECT * FROM people WHERE id = %s" %str(person_id) )
#    return str(query.cursor.fetchall())


#if request.method == 'GET':
#  def get_data_id(data_id):
#    return '%s' % data_id
#else if request.method == "DELETE":
#  def delete_data_id(data_id):
#    return '%s' % data_id


#TODO / plan:
  #
  # add tests




