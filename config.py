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
	cur.execute("CREATE TABLE IF NOT EXISTS user_table(id integer primary key autoincrement, name varchar(20) not null,	surname varchar(20) null, password varchar(20) null, email varchar(20) null)")
	db.commit()


if __name__ == "__main__":
	setup_db()



	  
