#Import necessary libraries and a database for application to work
import os
import sqlite3
import flask as fl
from flask import render_template, url_for, redirect, g, request
from contextlib import closing

import appMethods


app = fl.Flask(__name__)

DATABASE = 'app_db/appDB.db'

#Connect to the DB
def connect_db():#Get the connection to DB sorted out
    rw = fl.g._database = sqlite3.connect(DATABASE)    
    return rw

#Initiate call to DB
def get_db():
    db = getattr(fl.g, '_database', None)
    if db is not None:
        db = fl.g._database = sqlite3.connect(DATABASE)
        return db
    
	
#Teard down connection when it is not needed anymore
@app.teardown_appcontext
def close_db(exception):
    db = getattr(fl.g, "_database", None)
    if db is not None:
        db.close()


#Routing functions
@app.route("/")#Initial page that user sees when web app loads
def login():
    return  render_template('login.html')

@app.route("/signup", methods=['POST', 'GET'])#Page to register new users
def signup():
    if request.method == "POST":
        _name = request.args.get('inputName')
        _surname = request.args.get('inputSurname')
        _password = request.args.get('inputPassword')
        createuser(_name, _surname, _password)
        return render_template('home.html')
    else:
        return  render_template('signUp.html')


#this method will insert new users into user_table in the database
def createuser(name, surname, password):
    db = connect_db()
    cur = db.cursor()    
    cur.execute('INSERT INTO user_table(name, surname, password) VALUES (?, ?, ?)', (name, surname, password))
    db.commit()    
    db.close()

@app.route("/home")#Page that users see if they have signed in or registered
def home():    
    return  render_template('home.html')



if __name__ == "__main__":    
    app.run(debug = True)