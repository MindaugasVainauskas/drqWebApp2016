# This is the configuration file for the database that will be used by the application
# If database does not exist(first time running/database has been deleted) then this will create it.


from flask.ext.pymongo import PyMongo

mongo = PyMongo()
# file path to the database is defined
DATABASE = 'c:\data\db\webAppDB'

# setup the database for users who will use the application
def setup_db():

    mongo.db.createCollection("users")




if __name__ == "__main__":
    setup_db()
