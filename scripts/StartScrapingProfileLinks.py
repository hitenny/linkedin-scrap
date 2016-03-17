# -*- coding: utf-8 -*-
import csv
import unicodecsv
import os
from modules import Linkedin
from modules import KeywordFileReader
	    	
def search_doctors_from_file():
    first_run = "false"
		
    if(not os.path.isfile("last_processed")):
	first_run = "true"
	last_processed_profile = 0

	#Create the output file header	
	with open('profiles.csv', 'wb') as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames = [
							"NAME",
							"PROFILE NAME",
							"TITLE",
							"LOCATION", 
							"INDUSTRY",
							"PUBLIC PROFILE LINK", 
							"CURRENT WORK", 
							"PAST WORK", 
							"CONNECTIONS",
							"SUMMARY", 	
							"EDUCATION",
							"EXPERIENCE",
							"CURRENT TITLE",
							"SKILLS",
							"DOWNLOAD DATE",
							"PHOTO PRESENT",
							"PHOTO FILE NAME", ], 
							delimiter = ';')
	    writer.writeheader()
    else:
	lp = open("last_processed", 'r')
	last_processed_profile = int(lp.read())
	lp.close()
	
    with open('infiles/doctorlinks.csv', 'r') as doctorfile:
	rows = unicodecsv.reader(doctorfile, delimiter=',', encoding='ISO-8859-1')
	
	lt = Linkedin.LinkedinDownload()
	
	num_processed = 0
	for row in rows:

	    if(num_processed == 0):
	        num_processed = 1
		continue	

	    #Resume from last processed	
	    if num_processed < last_processed_profile+1:
		num_processed = num_processed+1
		continue

	    name = row[0]
	   
	    print "Processing profile [" + str(num_processed) + "] . Searching for " + name.encode('utf-8')
	    
	    ret = lt.searchPeople(row[0], row[1])

	    lp = open("last_processed", 'w+')
	    lp.write(str(num_processed))
	    lp.close()	
	    
	    num_processed = num_processed + 1
	    	
if __name__ == "__main__":
	search_doctors_from_file()
