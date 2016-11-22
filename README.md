## Single page web application project
#### Author: Mindaugas Vainauskas
#### Data representation and querrying module
#### 3rd Year Software Development Course
#### GMIT 2016

##Project description
Single page Web application using Flask microframework, Python, Bootstrap and MongoDB database. Database is hosted on mlab.com cloud platform. This is a one person project done by me, Mindaugas Vainauskas, for Data representation and querrying module. 3rd year software development course.

##Before Starting
- Download and install flask microframework from [Flask Website](https://pypi.python.org/pypi/Flask/0.11)
- Install flask_pymongo extension to be able to use MongoDB
- Install flask_scrypt extension for salt generation and password hashing.

##Running the application
This application can be run from command line of CMDr tool for windows (Available from [cmder website](http://cmder.net/)).
Alternatively it can be run from [Pycharm](https://www.jetbrains.com/pycharm/) Python IDE run menu.

##Using the application
  When loaded for the first time user is greeted by log-in window and needs to create a user account. This can be done by either clicking a link on top right of the window or link under log-in form. This will take them into sign-up page where users have to enter their username(must be unique!), email and password.

  Once sign-up process is completed they are taken to the home page and can see the options on navigation bar for adding new contact into the contact list, logging out of the app, and deleting the user account if they wish so.
  
####Home page
  Displays contact list with their full details and a delete button to delete contact from the list if user wants to. Before deleting a confirmation message prompts to make sure button was not clicked accidentally.
  
####Adding a contact
  Once user clicks on link to add new contact they are greeted by contact addition form where they add new contact's name, surname, phone number and email address. User can return to the home page by clicking home link on navigation bar.
  
####Log out
Allows user to log out of current contact list and brings them back to log-in page.

####Delete user account
Allows user to delete user acount together with contact list from the database if they wish so. User gets similar prompt to confirm the deletion of the account as when they are deleting a contact. Again this is done to prevent them accidentally pressing the button.

