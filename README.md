## Single page web application project
#### Author: Mindaugas Vainauskas
#### Data representation and querrying module
#### 3rd Year Software Development Course
#### GMIT 2016

##Project description
This is a Single Page Web application project done by me, Mindaugas Vainauskas, for Data representation and querrying module. 3rd year software development course, GMIT. Idea for this project comes from my wish for web-app that would be simple and easy to use. As such, a contact list web-app was deemed a good choice. Application itself is basic, but allows for depositing of user data on database, later retrieval of it and eventually deletion from database, if the user chooses so.

**Technologies used:** Flask microframework, Python, Bootstrap and MongoDB database. Database is hosted on [mlab](https://mlab.com) cloud platform. If required local database can also be used by replacing uri for MongoDB in app.config in python file with the path to local MongoDB location on the machine. Github is used to track development process of the application.

##Before Starting
- Download flask microframework from [Flask Website](https://pypi.python.org/pypi/Flask/0.11) and follow their installation guide for your platform.
- Install flask_pymongo extension to be able to use MongoDB.
- Install flask_scrypt extension for salt generation and password hashing.
- If you decide to use local MongoDB database you can download it for your platform from [MongoDB website](https://www.mongodb.com/download-center?jmp=nav) and follow the appropriate installation guide provided there.

##References
- MongoDB Tutorial: https://www.tutorialspoint.com/mongodb/
- Flask Documentation: http://flask.pocoo.org/docs/0.11/
- Bootstrap Components guide: http://getbootstrap.com/components/ 
- Jquery documentation for events(document and mouse used in project): http://api.jquery.com/category/events/

##Running the application
This application can be run from command line of CMDr tool for Windows (Available from [cmder website](http://cmder.net/)) or from Python script console on any Python IDE. Once started, it can be accessed from browser window by entering localhost url(localhost:5000).

#Short User guide

##Using the application
  When loaded for the first time user is greeted by log-in window and needs to create a user account. This can be done by either clicking a link on top right of the window or link under log-in form. This will take them into sign-up page where users have to enter their username, email and password. Username is enforced to be unique in the system by performing checks for existing username in database. If existing username is found it returns text to user that username has been taken already.

  Once sign-up process is completed they are taken to the home page and can see the options on navigation bar for adding new contact into the contact list, logging out of the app, and deleting the user account if they wish so.
  
####Home page
  Displays contact list with their full details and a delete button to delete contact from the list if user wants to. Before deleting a confirmation message prompts to make sure button was not clicked accidentally.
  
####Adding a contact
  Once user clicks on link to add new contact they are greeted by contact addition form where they add new contact's name, surname, phone number and email address. User can return to the home page by clicking home link on navigation bar.
  
####Log out
Allows user to log out of current contact list and brings them back to log-in page.

####Delete user account
Allows user to delete user acount together with contact list from the database if they wish so. User gets similar prompt to confirm the deletion of the account as when they are deleting a contact. Again this is done to prevent them accidentally pressing the button.

