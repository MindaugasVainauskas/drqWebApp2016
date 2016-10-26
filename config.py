#This is the configuration file for the database that will be used by the application
#If database does not exist(first time running/database has been deleted) then this will create it.

import sqlite3

#file path to the database is defined
DATABASE = 'app_db/appDB.db'

#setup the database for users who will use the application
def setup_db():
	db = sqlite3.connect(DATABASE)
	cur = db.cursor()

	#if the database does not exist get it created
	cur.execute("CREATE TABLE IF NOT EXISTS user_table(id integer primary key autoincrement, name varchar(20),	surname varchar(20), password varchar(192))")
	db.commit()

	#insert some dummy user data for testing purposes when DB is created.
	cur.execute("SELECT COUNT(*) FROM user_table")
	if cur.fetchall()[0][0] == 0:
		cur.execute('INSERT INTO user_table(name, surname, password) VALUES("admin", "adminas", "Admin1")')		
		db.commit()		

if __name__ == "__main__":
	setup_db()





































	  
