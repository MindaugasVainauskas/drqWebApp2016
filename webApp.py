# Import necessary libraries and a database for application to work

from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash


app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'usersDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/usersDB'


mongo = PyMongo(app)


# Routing functions
@app.route("/")  # Initial page that user sees when web app loads
def login():
    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])  # Page to register new users
def signup():
    if request.method == 'POST':
        salt = generate_random_salt()  # generate random salt for the new users password

        # check if user exists in DB
        user_exists = mongo.db.usersDB.find_one({'username': request.form['inputUsername']})

        if user_exists is None:
            username = request.form['inputUsername']  # take in the username from form input
            email = request.form['inputEmail']  # take in the email from form selection
            password = request.form['inputPassword']  # take in the password from form selection
            pass_hash = generate_password_hash(password, salt)  # generate password hash that will get stored in the DB
            # create user account
            createuser(username, email, pass_hash, salt)
            return redirect(url_for('home'))
        return 'User with such name exists!!!'
    else:
        return render_template('signUp.html')


# this method will insert new users into the collection in the database
def createuser(username, email, password, salt):
    # get user details from http page and put into mongoDB
    mongo.db.usersDB.insert({
        'username': username  # insert username into document
        , 'email': email  # insert email
        , 'password': password  # insert password hash
        , 'salt': salt  # insert salt that was used to generate password hash. To be used with login later
    })


@app.route('/home')  # Page that users see if they have signed in or registered
def home():
    # user = mongo.db.users.find_one({'username': username})
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
