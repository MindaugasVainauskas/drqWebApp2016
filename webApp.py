# Import necessary libraries and a database for application to work

from flask import Flask, render_template, url_for, request, redirect, session, json
from flask_pymongo import PyMongo
from flask_scrypt import generate_random_salt, generate_password_hash


app = Flask(__name__)

# get the database config files done
app.config['MONGO_DBNAME'] = 'usersdb'
app.config['MONGO_URI'] = 'mongodb://admin:admin@ds147487.mlab.com:47487/usersdb'

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
            return 'Wrong Password entered!!'  # if username matches but passwords doesnt this message is displayed
        return 'Wrong Username entered'  # if usernames don't match this message is displayed

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
        'username': username  # insert username into document
        , 'email': email  # insert email
        , 'password': password  # insert password hash
        , 'contacts': []  # array of objects for later to store contacts
        , 'salt': salt  # insert salt that was used to generate password hash. To be used with login later
    })


@app.route('/home', methods=['GET', 'POST'])  # Page that users see if they have signed in or registered
def home():
    if 'currentUser' in session:
        curr_user = session['currentUser']
        names = mongo.db.usersDB.find_one({'username': curr_user})
        return render_template('home.html', user=session['currentUser'])
    return render_template('login.html')


# Add the new contact into the list of contacts of the user.
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        cName = request.form['inputName']
        cSname = request.form['inputSurname']
        cPhone = request.form['inputPhone']
        cEmail = request.form['inputEmail']
        createcontact(cName, cSname, cPhone, cEmail)
    return render_template('contact.html', user=session['currentUser'])


@app.route("/retrieve", methods=['GET'])
def getcontacts():
    curr_user = session['currentUser']
    cursor = mongo.db.usersDB
    coNames = cursor.find_one({'username': curr_user})
    # get rid of parts of an object that are not json serialisable or unnecessary. like id, password and salt used.
    coNames.pop("_id")
    coNames.pop("password")
    coNames.pop("salt")
    return json.dumps(coNames)


# The following method creates contact based on given contact details.
def createcontact(cName, cSname, cPhone, cEmail):
    curr_user = session['currentUser']

    mongo.db.usersDB.update({'username': curr_user}, {'$push': {
        'contacts': {'name': cName, 'surname': cSname, 'phone': cPhone, 'email': cEmail}
    }
    })


@app.route('/del_contact', methods=['POST', 'GET'])
def del_contact():
    if request.method == 'POST':
        cEmail = request.values['cEmail']
        cPhone = request.values['cPhone']
        delete_contact(cEmail, cPhone)
        #return render_template('home.html')
        return cEmail+" "+cPhone


# The following method deletes contact.
def delete_contact(cEmail, cPhone):
    curr_user = session['currentUser']
    cursor = mongo.db.usersDB
    cursor.update({'username': curr_user},
                  {'$pull': {'contacts': {'email': cEmail, 'phone': cPhone}}})
    print('DELVALUES: --', cEmail, ' --', cPhone, '--', curr_user, '--')


# The following method route removes user document from database effectively deleting user account from web-app.
@app.route('/delete_user')
def delete_user():
    existing_user = session['currentUser']
    session.pop('currentUser', None)
    mongo.db.usersDB.remove({'username': existing_user})
    return redirect(url_for('login'))


# get the logout page working
@app.route('/logout')
def logout():
    session.pop('currentUser', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
