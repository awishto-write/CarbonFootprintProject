from flask import *
from werkzeug.local import LocalProxy
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import pymongo
import os
from dotenv import load_dotenv

app = Flask(__name__)
secret = os.getenv('url')
app.config["MONGO_URI"] = secret

mongo = PyMongo(app)
mongo.db.users.create_index([('email', pymongo.ASCENDING)], unique=True)




@app.route("/")
def test():
    print("This is a test message.")
    return "Request successful"

@app.route("/login")
def login_and_auth():
    return "Test message"

@app.route("/create_user", methods=["POST"])
def createUser():
    if not request.json or not 'user_id' in request.json or not 'email' in request.json or not 'password' in request.json or not 'footprint' in request.json:
        abort(400)


    try:
        user_id = request.json['user_id'] 
        email = request.json['email']
        password = request.json['password']
        footprint = request.json['footprint']

        userDocument = {'user_id': user_id, 'email': email, 'password': password, 'footprint': footprint}
        mongo.db.users.insert_one(userDocument)
        return ("Insert Successful!")
    except pymongo.errors.DuplicateKeyError:
        return ("A user with that email already exists.")
    except:
        return "Something went wrong. Please try again."
    