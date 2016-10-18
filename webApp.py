from flask import Flask, render_template, url_for, redirect


app = Flask(__name__)

@app.route("/")
def index():
    return  render_template('index.html')#return function returns premade text with the name added to the end.

@app.route("/signup")
def signup():
    return  render_template('signUp.html')

@app.route("/login")
def login():
    return  render_template('login.html')

@app.route("/")
def home():
    return  render_template('home.html')
#Managed to get the templates routing working thanks to: http://flask.pocoo.org/docs/0.11/quickstart/#routing


if __name__ == "__main__":
    app.run(debug=True)