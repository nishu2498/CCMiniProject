# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import json
import cars as cars
from flask import Flask,request


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# rule = request.url_rule

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'
# def respond(self, status_code, message=None):
#     """
#     Sends response back to client
#     :param status_code: response HTTP status code
#     :param message: optional response message (example: JSON)
#     """
#     self.send_response(status_code)
#     self.send_header('Content-type', 'application/json')
#     self.end_headers()
#     if message is not None:
#         self.wfile.write(bytes(message, "utf8"))

def is_body_valid(_body, _keys):
    """
    Checks if body contains all attributes necessary for a "Car" object.
    :param _body: dictionary object to be checked
    :param _keys: keys required to be in dictionary
    :return: True if body contains all _keys and only those, False otherwise
    """
    # check number of keys
    body_keys = set(_body.keys())
    if len(body_keys) != len(_keys):
        return False

    # check if body keys match required keys
    if len([key for key in _keys if key not in _body]) > 0:
        return False

    return True

@app.route("/cars",methods=["GET"])
def do_cars():
   return cars.get_cars(),HTTPStatus.OK 
    

@app.route("/car/<id>",methods=["GET"])
def do_car(id=0):  
    car = cars.get_car(id)
    if car is None:  # car not found
        return HTTPStatus.NOT_FOUND

    return car,HTTPStatus.OK

@app.route("/cars",methods=["POST"])
def do_POST():
   
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        post_body = request.json
    else:
        return "no content",HTTPStatus.NO_CONTENT
    # post_body = request.json
    post_body_string = json.dumps(post_body)
    # load post body into a dictionary object
    try:
            body = json.loads(post_body_string)
    except json.JSONDecodeError:
        return "bad request",HTTPStatus.BAD_REQUEST

    # check validity of body
    required_keys = ("id", "make", "model", "year", "price")
    if is_body_valid(body, required_keys) is False:
        return "unprocessable entity",HTTPStatus.UNPROCESSABLE_ENTITY
        

    # check for duplicate ids
    car = cars.get_car(body["id"])
    if car is not None:
        return "Data conflict",HTTPStatus.CONFLICT

    # all good, add car
    cars.insert(body)
    return "Data Inserted!!!",HTTPStatus.ACCEPTED

@app.route("/car/<id>",methods=["PUT"])
def do_PUT(id=0):
   
    car = cars.get_car(id)
    if car is None:  # car not found
        return "not found",HTTPStatus.NOT_FOUND

    # get PUT body
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        post_body = request.json
    else:
        return "No content",HTTPStatus.NO_CONTENT

    # json dump the request post body
    post_body_string = json.dumps(post_body)
    # load PUT body into a dictionary object
    try:
        body = json.loads(post_body_string)
    except json.JSONDecodeError:
        return "Bad request",HTTPStatus.BAD_REQUEST
        

    # check validity of body
    required_keys = ("make", "model", "year", "price")
    if is_body_valid(body, required_keys) is False:
        return "Unprocessable entity",HTTPStatus.UNPROCESSABLE_ENTITY
        

    # all good, update car
    cars.update(id, body)
    return "Data Modified!!!",HTTPStatus.ACCEPTED

@app.route("/car/<id>",methods=["DELETE"])
def do_DELETE(id=0):

    car = cars.get_car(id)
    if car is None:  # car not found
        return "data not found",HTTPStatus.NOT_FOUND

    # delete car
    cars.delete(id)
    return "data deleted!!!",HTTPStatus.ACCEPTED
# class RestHandler(BaseHTTPRequestHandler):


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
