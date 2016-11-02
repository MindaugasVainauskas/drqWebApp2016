# Import necessary libraries and a database for application to work

import flask as fl
from flask import render_template, url_for, redirect, g, request
from flask_pymongo import PyMongo


app = fl.Flask(__name__)


app.config['MONGO_DBNAME'] = 'usersDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/usersDB'


mongo = PyMongo(app)


# Routing functions
@app.route("/")  # Initial page that user sees when web app loads
def login():
    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])  # Page to register new users
def signup():
    if request.method == "POST":
        username = request.values['inputUserName']
        email = request.values['inputEmail']
        password = request.values['inputPassword']
        # create user account
        createuser(username, email, password)
        return render_template('home.html')
    else:
        return render_template('signUp.html')


# this method will insert new users into user_table in the database
def createuser(username, email, password):
    # get user details from http page and put into mongoDB
    mongo.db.usersDB.insert({
        username: "name"
        , email: "email"
        , password: "password"
    })


@app.route('/home/<username>')  # Page that users see if they have signed in or registered
def home(username):
    user = mongo.db.users.find_one_or_404({'name': username})
    return render_template('home.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
