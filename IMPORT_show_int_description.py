#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import MySQLdb
import re
# import csv # not needed right now
# import time # not needed right now

#Create var for Date in Filename Label
CurrentDate = (time.strftime("%m_%d_%Y"))

## Some csv creation stuff, circle back later if I need it
	#Create string for filename path
	#CreateFile = os.path.join('./CSV_Export_'+CurrentDate+".csv")
	#print "New File " + CreateFile + " created or opened"
	#print CreateFile + " in progress"
	#Open/Create csv file for export - opening a file that doesn't exist creates new file. Displays error message if file already exists.

	#if os.path.exists(os.path.join('./CSV_Export_'+CurrentDate+".csv")):
	#	print "Error  " './CSV_Export_'+CurrentDate+".csv' alyready exists in this directory, please delete or move this file before running the script again"

	#else:
		#FileName = open(CreateFile, 'w')
		#FileName.close()
	#csv writer, not working --- OutputFile = open(CreateFile, 'w')
	#csv writer, not working --- writer = csv.DictWriter(OutputFile, fieldnames=fieldnames)

fieldnames = [ 'Router_Name', 'Int', 'Int Status', 'Int Protocol', 'Int Description']


db_connect = MySQLdb.connect("localhost","root","cisco123","inventory_data")
db_cursor = db_connect.cursor()

for root, dirs, files in os.walk('.'):
	for file in files:
		if file.endswith(("description.txt")):
			#remove trailing ' -show_interfaces_description.txt' from .txt name, save as DB_Router_Name and print via  slice
			DB_Router_Name = file[:-32]

			#print DB_Router_Name - Debug print command
			#print root - Debug print command

			pathVAR = os.path.join(root, file)
			#print pathVAR
			# open file and  find interfaces
			OpenTXT = open(pathVAR , 'r')
			print OpenTXT # nice side effect of scrolling the router names as they are iterated, keep me in.


			# read line by line, skipping the first 4
			lines = OpenTXT.readlines()[4:]

			


			for line in lines:
				#print DB_Router_Name + "," + line;

				#simple regex to split the line by whitespace, generates a LineOut list to give the specific fields
				LineOut = re.split("\s*",line,3)

				#string literal error fix - extra stripme variables pull the whitespace out of the regex'd fields, 
				DB_Int_stripme = LineOut[0]
				DB_Int = DB_Int_stripme.strip()

				DB_Int_Status_stripme = LineOut[1]
				DB_Int_Status = DB_Int_Status_stripme.strip()

				DB_Int_Protocol_stripme = LineOut[2]
				DB_Int_Protocol = DB_Int_Protocol_stripme.strip()

				DB_Int_Description_stripme = LineOut[3]
				DB_Int_Description = DB_Int_Description_stripme.strip()

				#print DB_Router_Name,DB_Int,DB_Int_Status,DB_Int_Protocol,DB_Int_Description   ---- Used for Debugging

				Field_Input = "INSERT INTO ShowIntDescription (router, interface, status, protocol, description) VALUES (%s,%s,%s,%s,%s)" 

				#Cursor doesn't work with variables as arguments and for some reason can't handle the Field_Input with %s defined, but has built in functionality in the .execute that makes this actually work so the DB... variables in () actually instert into the %s from the Field_Input - working!

				db_cursor.execute(Field_Input, (DB_Router_Name, DB_Int, DB_Int_Status, DB_Int_Protocol, DB_Int_Description) )

				
				#csv writer, not working --- writer.writerow({ 'Router_Name' : DB_Router_Name , 'Int' : DB_Int , 'Int Status' : DB_Int_Status , 'Int Protocol' : DB_Int_Protocol, 'Int Description' : DB_Int_Description }) # gives bad output, I think its an encoding problem but I couldn't fix, try again later?

				
			print " Export Done"


#do I actually need this?, doesn't seem to be hurting anything...
db_connect.commit()
db_connect.close()


#	OutputFile.close()
#	OpenTXT.close()

