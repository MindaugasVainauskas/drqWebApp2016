#Import necessary libraries and a database for application to work
import sqlite3
from flask import Flask, render_template, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy#database connector for flask?
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config')#configuration for the app comes from config.py file in the same folder
db = SQLAlchemy(app)


def connect_db():#Get the connection to DB sorted out
    return sqlite3.connect(app.config['DATABASE'])

#Initialise the DB for Application
def init_db():
    with closing(connect_db) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.cli.command('initdb')
def initdb_command():    
    init_db()
    print ('Initialized the database.')

@app.route("/")#Initial page that user sees when web app loads
def login():
    return  render_template('login.html')

@app.route("/signup")#Page to register new users
def signup():
    return  render_template('signUp.html')

@app.route("/home")#Page that users see if they have signed in or registered
def home():
    return  render_template('home.html')



if __name__ == "__main__":
    app.run()