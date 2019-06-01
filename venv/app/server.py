# to start app, cd to same directory and : FLASK_APP=server.py flask run

from flask import Flask, request
from sqlalchemy import create_engine



db_connect = create_engine('sqlite:///rest_api.db')
app = Flask(__name__)



@app.route("/resources/data", methods = ["GET"])
def put_person():
    conn = db_connect.connect()
    query = conn.execute("select * from people")
    return str(query.cursor.fetchall())
    # use request.form() to validate the data posted and write it to the database.


@app.route("/resources/data/<string:person_id>", methods = ["GET", "DELETE"])
def get_person(person_id):
    conn = db_connect.connect()
    query = conn.execute("SELECT * FROM people WHERE id = %s" %str(person_id) )
    return str(query.cursor.fetchall())


#if request.method == 'GET':
#  def get_data_id(data_id):
#    return '%s' % data_id
#else if request.method == "DELETE":
#  def delete_data_id(data_id):
#    return '%s' % data_id


#TODO / plan:
  #
  # add tests




