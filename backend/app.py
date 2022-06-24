from flask import *
import os

app = Flask(__name__)

@app.route("/")
def test():
    print("This is a test message.")
    return "Request successful"