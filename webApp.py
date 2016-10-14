from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return  app.send_static_file('index.html')#return function returns premade text with the name added to the end.
	
@app.route("/<name>", methods=['GET', 'POST'])#route command gets /name/<insert whatever name here>
def name(name):
    return  'Your name is ' + request.args.get("name")


#Managed to get the templates routing working thanks to: http://flask.pocoo.org/docs/0.11/quickstart/#routing


if __name__ == "__main__":
    app.run(debug=True)