from flask import *
from werkzeug.local import LocalProxy
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from firebase_admin import credentials, auth
import pymongo
import os
import pyrebase
import firebase_admin

template_dir = os.path.abspath('../frontend/templates/')
static_dir = os.path.abspath('../frontend/static/')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

secret = os.getenv('url')
app.config["MONGO_URI"] = secret

mongo = PyMongo(app)
mongo.db.users.create_index([('email', pymongo.ASCENDING)], unique=True)
mongo.db.users.create_index([('username', pymongo.ASCENDING)], unique=True)

cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbConfig.json')))



@app.route("/")
def index():
    if 'user' in session:
        return "Login page but when someone is logged in"
    else:
        return render_template('home_page.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return "You're already logged in!"
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
        except:
            return 'Failed to login. Username and/or password may be incorrect.'
    else:
        return render_template('Login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')
    else:
        return "No user is logged in."

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        if 'user' in session:
            email = request.form.get('email')
            auth.send_password_reset_email(email)
            return 'Password reset email sent'
        else:
            return 'Please log in first.'
    else:
        return "i forgor"

 
@app.route("/create_user", methods=["GET","POST"])
def createUser():
    if 'user' in session:
        return "You're already logged in!"
    else:
        if request.method == "POST":

            email_a = request.form.get('email')
            password_a = request.form.get('password')
            username = request.form.get('username')

            if email_a is None or password_a is None or username is None:
                return {'message': 'Error! Missing username, email or password'}, 400

            try:

                userDocument = {'user_id': "", 'username': username, 'email': email_a, 'password': password_a, 'electric_bill': 0, 
                'gas_bill': 0, 'oil_bill': 0, 'mileage': 0, 'flights_less': 0, 'flights_greater': 0,
                'recycle_paper': False, 'recycle_cans': False,'footprint': 0}
                mongo.db.users.insert_one(userDocument)
                
            except pymongo.errors.DuplicateKeyError:
                return ("A user with that username or email already exists.")
            except:
                return "Something went wrong. Please try again."

            try:
                user = auth.create_user(email=email_a, password=password_a)
                filter = {'email': email_a}
                newvalues = {"$set": {'user_id': user.uid}}
                mongo.db.users.update_one(filter, newvalues)
                return {'message': f'Successfully created user {user.uid}'}, 200
            except:
                return {'message': 'Error! Something went wrong. Please try again'}, 400
        
        else:
            return render_template('SignUp.html')

@app.route("/setup_user_step_1", methods=["GET", "POST"])
def setupUserStep1():
    if 'user' in session:
        if request.method == "POST":
            electric_bill = request.form.get("electric_bill")
            filter = {'email': session['user']}
            newvalues = {"$set": {'electric_bill': electric_bill}}
            mongo.db.users.update_one(filter, newvalues)
            return "Electric bill updated successfully."
        else:
            return "Elec. bill question here"
    else:
        return "No user is logged in."


@app.route("/setup_user_step_2", methods=["GET", "POST"])
def setupUserStep2():
    if 'user' in session:
        if request.method == "POST":
            gas_bill = request.form.get("gas_bill")
            filter = {'email': session['user']}
            newvalues = {"$set": {'gas_bill': gas_bill}}
            mongo.db.users.update_one(filter, newvalues)
            return "Gas bill updated successfully."
        else:
            return "Gas bill question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_3", methods=["GET", "POST"])
def setupUserStep3():
    if 'user' in session:
        if request.method == "POST":
            oil_bill = request.form.get("oil_bill")
            filter = {'email': session['user']}
            newvalues = {"$set": {'oil_bill': oil_bill}}
            mongo.db.users.update_one(filter, newvalues)
            return "Oil bill updated successfully."
        else:
            return "Oil bill question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_4", methods=["GET", "POST"])
def setupUserStep4():
    if 'user' in session:
        if request.method == "POST":
            mileage = request.form.get("mileage")
            filter = {'email': session['user']}
            newvalues = {"$set": {'mileage': mileage}}
            mongo.db.users.update_one(filter, newvalues)
            return "Mileage updated successfully."
        else:
            return "Mileage question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_5", methods=["GET", "POST"])
def setupUserStep5():
    if 'user' in session:
        if request.method == "POST":
            flights_less = request.form.get("flights_less")
            filter = {'email': session['user']}
            newvalues = {"$set": {'flights_less': flights_less}}
            mongo.db.users.update_one(filter, newvalues)
            return "Flights < 4 updated successfully."
        else:
            return "Flights < 4 question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_6", methods=["GET", "POST"])
def setupUserStep6():
    if 'user' in session:
        if request.method == "POST":
            flights_greater = request.form.get("flights_greater")
            filter = {'email': session['user']}
            newvalues = {"$set": {'flights_greater': flights_greater}}
            mongo.db.users.update_one(filter, newvalues)
            return "Flights >= 4 updated successfully."
        else:
            return "Flights >= 4 question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_7", methods=["GET", "POST"])
def setupUserStep7():
    if 'user' in session:
        if request.method == "POST":
            recycle_paper = request.form.get("recycle_paper")
            filter = {'email': session['user']}
            newvalues = {"$set": {'recycle_paper': recycle_paper}}
            mongo.db.users.update_one(filter, newvalues)
            return "Paper Recycle updated successfully."
        else:
            return "Paper Recycle question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_step_8", methods=["GET", "POST"])
def setupUserStep8():
    if 'user' in session:
        if request.method == "POST":
            recycle_cans = request.form.get("recycle_cans")
            filter = {'email': session['user']}
            newvalues = {"$set": {'recycle_cans': recycle_cans}}
            mongo.db.users.update_one(filter, newvalues)
            return "Cans Recycle updated successfully."
        else:
            return "Cans Recycle question here"
    else:
        return "No user is logged in."

@app.route("/setup_user_final", methods=["GET"])
def setupUserFinal():
    if 'user' in session:
        total_sum = 0
        for x in mongo.db.users.find({},{"email": session['user']}):
            total_sum = total_sum + (x['electric_bill'] * 105) + (x['gas_bill'] * 105) + (x['oil_bill'] * 113)
            total_sum = total_sum + (x['mileage'] * 0.79)
            total_sum = total_sum + (x['flights_less'] * 1100) + (x['flights_greater'] * 4400)
            if x['recycle_paper'] == False:
                total_sum = total_sum + 184
            if x['recycle_cans'] == False:
                total_sum = total_sum + 166
        return "Your carbon footprint is " + str(total_sum) + "."
            

    else:
        return "No user is logged in."
    