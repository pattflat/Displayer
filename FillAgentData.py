import time
import sys
import datetime
import sqlite3

def insert_inscription_to_db(mytable,myarray):         

	from datetime import datetime

	#Open SQL DB
	db=sqlite3.connect("WEBAgent.db")
	c=db.cursor()
	stmt = "SELECT name FROM sqlite_master WHERE type='table' and name = '" + mytable + "'"
	c.execute(stmt)
	result = c.fetchone()
	if result:
		print "Refreshing Data : need to delete it first"
		c.execute("""DELETE FROM %s"""% mytable) 
	else:
		c.execute("""CREATE TABLE %s (img TEXT,address TEXT,city TEXT,price TEXT)"""% mytable) 
	
	db.commit()
	line = " "

	while(line != None):
		line = c.fetchone()
		print line

	print "********************* Start Import Inscriptions **************************"
	timestart = datetime.now()
	print myarray
        print mytable
	c.executemany("""INSERT INTO %s(img,address,city,price)\
							VALUES( ?, ?, ?, ?)""" %mytable,(myarray))


	timeend = datetime.now()
	print "Insert Took : " + str((timeend - timestart))
	#close the connection to the database.
	db.commit()
	c.close()
	print "********************* Done **************************"


def insert_main_info_to_db(image,name,imgphone,phone,data,last_display,count):         

	from datetime import datetime
	
	mytable = "agentview"
	#Open SQL DB
	db=sqlite3.connect("WEBAgent.db")
	c=db.cursor()
	stmt = "SELECT name FROM sqlite_master WHERE type='table' and name = '" + mytable + "'"
	c.execute(stmt)
	result = c.fetchone()
	if result:
		print "Table Already Exist .. Using it..."
	else:
		c.execute("""CREATE TABLE %s (img TEXT,name TEXT UNIQUE,imgphone TEXT,phone TEXT,data TEXT,last_display TEXT,count TEXT)"""% mytable) 

	db.commit()
	line = " "


	print "********************* Start Import **************************"
	timestart = datetime.now()
	try:
		c.execute("""INSERT INTO %s (img,name,imgphone,phone,data,last_display,count)\
	 VALUES(?, ?, ?, ?, ?, ?, ?)""" %mytable, (image,name,imgphone,phone,data,last_display,count))
	except sqlite3.OperationalError, msg:
		print "op error:"
		print msg
	except sqlite3.IntegrityError, msg:
		c.execute("""UPDATE %s SET img = ?, imgphone = ?, phone = ?, data = ?, count = ? WHERE name = ?""" %mytable,(image,imgphone,phone,data,count,name))
		
	timeend = datetime.now()
	print "Insert Took : " + str((timeend - timestart))
	#close the connection to the database.
	db.commit()
	c.close()
	print "********************* Done **************************"

