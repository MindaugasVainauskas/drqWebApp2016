#Import necessary libraries and a database for application to work
import os
import sqlite3
from flask import Flask, render_template, url_for, redirect, g
from contextlib import closing


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	#Configuration settings for the application 
	DATABASE= os.path.join(app.root_path, 'webApp.db'),#database location url
	USERNAME='admin',#user name for admin
	PASSWORD='admin',#password for admin
	SECRET_KEY='secret18',#secret key will be needed to secure client side connections to the server
	DEBUG = True #Switch on debug mode so its easy to see changes to app on the fly
))


#Connect to the DB
def connect_db():#Get the connection to DB sorted out
    rw = sqlite3.connect(app.config['DATABASE'])
    rw.row_factory = sqlite3.Row
    return rw

#Initiate call to DB
def get_db():
	if not hasattr(g, 'webApp_db'):
		g.webApp_db = connect_db()
	return g.webApp_db
	
#Teard down connection when it is not needed anymore
@app.teardown_appcontext
def close_db(error):
    
    if hasattr(g, 'webApp_db'):
        g.webApp_db.close()

#Originally adapted from http://flask.pocoo.org/docs/0.11/tutorial/dbinit/#tutorial-dbinit
#Initialise the DB for Application
def init_db():
    with closing(connect_db) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.cli.command('initdb')#overriding flask cli to include initdb command
def initdb_command():    
    init_db()    

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
    #init_db()
    app.run()