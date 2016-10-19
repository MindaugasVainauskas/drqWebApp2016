#Import necessary libraries and a database for application to work
import sqlite3
from flask import Flask, render_template, url_for, redirect, g
from contextlib import closing


#Configuration settings for the application 
DATABASE = '/tmp/webApp.db'#database location url
USERNAME = 'admin'#user name for admin
PASSWORD = 'admin'#password for admin
SECRET_KEY = 'secret18'#secret key will be needed to secure client side connections to the server
DEBUG = True #Switch on debug mode so its easy to see changes to app on the fly

app = Flask(__name__)
app.config.from_object(__name__)


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
        



@app.route("/")
def login():
    return  render_template('login.html')#return function returns premade text with the name added to the end.

@app.route("/signup")
def signup():
    return  render_template('signUp.html')

@app.route("/home")
def home():
    return  render_template('home.html')


#Managed to get the templates routing working thanks to: http://flask.pocoo.org/docs/0.11/quickstart/#routing


if __name__ == "__main__":
    app.run()