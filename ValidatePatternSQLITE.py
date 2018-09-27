import MySQLdb
import glob
import csv
import time
import sys
import sqlite3

if __name__ == '__main__':         

	if len(sys.argv) < 3:
		print "Missing Instance Parameters"
		print "Example : script.py table NbrPolicy(16-20 by Ports)" 
		print "Example : script.py FlowMeterC0210008 40" 
		exit()

	else:
		print 'Number of arguments:', len(sys.argv), 'arguments.'
		print 'Argument List:', str(sys.argv)

	mytable = sys.argv[1]
	myNbrOfPolicy = int(sys.argv[2])

	#Open SQL DB
	db=sqlite3.connect("FlowMeterTest.db")
	c=db.cursor()
	

	c.execute("""SELECT Period, COUNT(*) TotalCount\
			FROM %s\
			GROUP BY Period\
			HAVING COUNT(*) > 1\
			ORDER BY Period ASC"""% mytable)

	item = ""
	Period = 0
	BeforePeriod = 0
	Policy = 0
	BeforePolicy = 0
	while(item != None):
		item = c.fetchone()
		if(item == None): 
			break
		Period = int(item[0])
		Policy = int(item[1])
		if(BeforePeriod+1 != Period and BeforePeriod != 0):
			print "Error with Period : %s %s"%(BeforePeriod,BeforePolicy)			
			print "Error with Period : %s %s Sequence Broken"%(Period,Policy)
		elif(Policy != myNbrOfPolicy):
			print "Nbr Policy            : %s (Normally)"%(myNbrOfPolicy)			
			print "Error with Nbr Policy : %s %s (Got)"%(Period,Policy)

		BeforePeriod = Period
		BeforePolicy = Policy

	c.close()
	print "********************* Done **************************"

