# -*- coding: utf-8 -*-
import csv
import unicodecsv
import os
import sys
sys.path.append(os.path.abspath('modules'))
import Linkedin
import KeywordFileReader
from Util import createdirifnotexists,fileexistordie,gettimestamp

HOME = ""	    	
def search_doctors_from_file():
    first_run = "false"

    dirpath = "Results_" + gettimestamp()
    createdirifnotexists(dirpath)
    createdirifnotexists(dirpath + "/R0_profiles_raw/")		
    if(not os.path.isfile("last_processed")):
	first_run = "true"
	last_processed_profile = 0

        outfile = dirpath + "/R0_profiles_raw/" + "profiles-final.csv" 	
	#Create the output file header
	with open(outfile, 'wb') as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames = [
							"REQ ID",
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
	
    fileexistordie('infiles/doctors.csv')

    with open('infiles/doctors.csv', 'r') as doctorfile:
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

	    name = row[2] + " " + row[1]
	   
	    print "Processing profile [" + str(num_processed) + "] . Searching for " + name.encode('utf-8')
	    
	    ret = lt.search(row[2], row[1], row[0], dirpath)

	    lp = open("last_processed", 'w+')
	    lp.write(str(num_processed))
	    lp.close()	
	    
	    num_processed = num_processed + 1

    lt.dumpSummary()
	    	
if __name__ == "__main__":
	search_doctors_from_file()
