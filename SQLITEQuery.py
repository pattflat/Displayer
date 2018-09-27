
import time
import sys
import sqlite3

if __name__ == '__main__':         

	if len(sys.argv) < 2:
		print "Missing Instance Parameters" 
		print "Example : script.py query" 
		exit()

	else:
		print 'Number of arguments:', len(sys.argv), 'arguments.'
		print 'Argument List:', str(sys.argv)

	myquery = sys.argv[1]


	#Open SQL DB
	db=sqlite3.connect("WEBAgent.db")
	c=db.cursor()
	

	c.execute("""%s"""% myquery)

	item = ""

	while(item != None):
		item = c.fetchone()
		print item

	c.close()
	print "********************* Done **************************"

