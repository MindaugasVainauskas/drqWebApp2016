# Import necessary libraries and a database for application to work
from flask import Flask, render_template, url_for, request, redirect, session, json
from flask_pymongo import PyMongo
from flask_scrypt import generate_random_salt, generate_password_hash


app = Flask(__name__)

# Database name and URI for server that stores it. I am using mlab.com site to store the MongoDB that I'm using.

app.config['MONGO_DBNAME'] = 'usersdb'
app.config['MONGO_URI'] = 'mongodb://admin:admin@ds159377.mlab.com:59377/usersdb'


app.secret_key = 'mv_secret_key'  # need to have secret key to use session


mongo = PyMongo(app)


# Routing functions
@app.route("/")  # Initial page that user sees when web app loads
def root():
    # simply redirect users to login page as that is what they will need to see
    return redirect(url_for('login'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # find the user in database by username entered
        returning_user = mongo.db.usersDB.find_one({'username': request.form['inputName']})
        if returning_user is not None:
            saltUsed = returning_user['salt'] # get the salt used for password for this user
            passCheck = returning_user['password'] # get the password hash from database to compare passwords
            # next need to check that password entered corresponds to password that exists in the database for this user
            if generate_password_hash(request.form['inputPassword'], saltUsed) == passCheck:
                session['currentUser'] = returning_user['username']
                return redirect(url_for('home'))
            return render_template('WrongDetails.html')  # template with message is returned if username doesn't match
        return render_template('WrongDetails.html') # template with message is returned if password doesn't match

    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])  # Page to register new users
def signup():
    if request.method == 'POST':
        salt = generate_random_salt()  # generate random salt for the new users password

        # check if user exists in DB. This is done to enforce unique usernames.
        user_exists = mongo.db.usersDB.find_one({'username': request.form['inputUsername']})

        if user_exists is None:
            username = request.form['inputUsername']  # take in the username from form input
            email = request.form['inputEmail']  # take in the email from form selection
            password = request.form['inputPassword']  # take in the password from form selection
            pass_hash = generate_password_hash(password.encode('Utf-8'), salt)  # generate password hash that will get stored in the DB
            # create user account
            createuser(username, email, pass_hash, salt)
            session['currentUser'] = request.form['inputUsername']
            return redirect(url_for('home'))
        return 'User with such name exists!!!'  # if username is found in database the message is shown
    else:
        return render_template('signUp.html')  # if no form details present then normal signup page is shown


# this method will insert new users into the collection in the database
def createuser(username, email, password, salt):
    # get user details from http page and put into mongoDB
    mongo.db.usersDB.insert({
        'username': username # insert username into document
        , 'email': email # insert email
        , 'password': password # insert password hash
        , 'contacts': [] # array of objects for later to store contacts
        , 'salt': salt  # insert salt that was used to generate password hash. To be used with login later
    })


# Page that users see if they have signed in or registered
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'currentUser' in session:
        return render_template('home.html', user=session['currentUser'])
    return render_template('login.html')


# Add the new contact into the list of contacts of the user.
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        # get contact details from input form
        cName = request.form['inputName']
        cSname = request.form['inputSurname']
        cPhone = request.form['inputPhone']
        cEmail = request.form['inputEmail']
        # send details into create contact method
        createcontact(cName, cSname, cPhone, cEmail)
    return render_template('contact.html', user=session['currentUser'])


# this method route retrieves contact list from the database and sends it to be displayed in home page.
@app.route("/retrieve", methods=['GET'])
def getcontacts():
    curr_user = session['currentUser']
    cursor = mongo.db.usersDB
    coNames = cursor.find_one({'username': curr_user})  # gets the attributes for this user, including contact list.
    # get rid of parts of an object that are not json serialisable or unnecessary. like id, password and salt used.
    coNames.pop("_id")
    coNames.pop("password")
    coNames.pop("salt")
    coNames.pop("email")
    # send contacts list to the home page.
    return json.dumps(coNames)


# The following method creates contact based on given contact details.
def createcontact(cName, cSname, cPhone, cEmail):
    curr_user = session['currentUser']
    mongo.db.usersDB.update({'username': curr_user}, {'$push': {
        'contacts': {'name': cName, 'surname': cSname, 'phone': cPhone, 'email': cEmail}
    }
    })


# this method route gets the details of contact that needs to be deleted by accepting jquery from home page.
@app.route('/del_contact', methods=['POST', 'GET'])
def del_contact():
    if request.method == 'POST':
        cName = request.values['cName']
        cSurname = request.values['cSurname']
        cEmail = request.values['cEmail']
        cPhone = request.values['cPhone']
        delete_contact(cName, cSurname, cEmail, cPhone)


# The following method deletes contact from the list.
def delete_contact(cName, cSurname, cEmail, cPhone):
    curr_user = session['currentUser']
    cursor = mongo.db.usersDB
    cursor.update({'username': curr_user},
                  {'$pull': {'contacts': {'name': cName, 'surname': cSurname, 'email': cEmail, 'phone': cPhone}}})


# The following method route removes user document from database effectively deleting user account from web-app.
@app.route('/delete_user')
def delete_user():
    existing_user = session['currentUser']
    session.pop('currentUser', None)
    mongo.db.usersDB.remove({'username': existing_user})
    return redirect(url_for('login'))


# Log out page for new user to be able to use the web-app
@app.route('/logout')
def logout():
    session.pop('currentUser', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
