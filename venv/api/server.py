# Purpose: create a basic REST interface that can store and retrieve people information
#
# To start app, from the same directory as this file, run from the command line:
#   FLASK_APP=server.py FLASK_ENV=development flask run

from flask import Flask, request, json
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import os 

CURRENT_ENV = os.environ.get("FLASK_ENV", default='development')

if CURRENT_ENV == 'development':
  db_connect = create_engine('sqlite:///rest_api.db')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

app = create_app()
api = Api(app)




def return_person_json(person_id):
  conn = db_connect.connect()
  query = conn.execute("SELECT * FROM people WHERE id = %s" %str(person_id))
  person_list = query.cursor.fetchall()[0]
  return json.jsonify(id=person_list[0],
                      name=person_list[1],
                      age=person_list[2],
                      locale=person_list[3])

class People(Resource):
  def get(self, person_id):
    try:
      return return_person_json(person_id)
    except Exception:
      return "Encountered an error. Are you sure the person ID you requested exists?"

  def delete(self, person_id):
    try:
      person_json = return_person_json(person_id)
      conn = db_connect.connect()
      query = conn.execute("DELETE FROM people WHERE id = %s;" %str(person_id))
      return person_json
    except Exception:
      return "Failed to delete person with ID %s, are you sure this ID exists?".format(person_id)

class NewPeople(Resource):
  def put(self):
    try:
      conn = db_connect.connect()
      new_person_dict = json.loads(request.form['data'])
      query = conn.execute("INSERT INTO people (name, age, locale) \
                            VALUES ('{}', {}, '{}');".format(new_person_dict['name'], new_person_dict['age'], new_person_dict['locale']) )
      # Note: last_insert_rowid returns the rowid for the latest insert from this connection,
      #  so using it will not result in concurrency issues.
      query_inserted_id = conn.execute("select last_insert_rowid();")
      new_person_id = query_inserted_id.fetchall()[0][0]
      return json.jsonify(id=new_person_id,
                    name=new_person_dict['name'],
                    age=new_person_dict['age'],
                    locale=new_person_dict['locale'])
    except Exception:
      return "Failed to create person with Name".format(new_person_dict['name'])

api.add_resource(People, '/resources/data/<string:person_id>')
api.add_resource(NewPeople, '/resources/data/')




