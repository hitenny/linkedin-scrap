# -*- coding: utf-8 -*-
import csv
import os
import unicodecsv
import unicodedata
from Util import createdirifnotexists,fileexistordie,gettimestamp

#Input files
configdir = "Config_" + gettimestamp()
fileexistordie(configdir)

summarypath = "Summary_" + gettimestamp()
createdirifnotexists(summarypath)
s2dir = summarypath + "/S2_HPU_PROC/"
createdirifnotexists(s2dir)


hiCorrectFile = configdir + "/C2_HPU_raw/" + "HI_correct.csv"
uiCorrectFile = configdir + "/C2_HPU_raw/" + "UI_correct.csv"
fileexistordie(hiCorrectFile)
fileexistordie(uiCorrectFile)

#Output files
parentdir = "Results_" + gettimestamp()
createdirifnotexists(parentdir)

procdir = parentdir + "/R2_profiles_HPU_proc/"
createdirifnotexists(procdir)

hiProcessedFile = parentdir + "/R2_profiles_HPU_proc/" + "HI_processed.csv"
piProcessedFile = parentdir + "/R2_profiles_HPU_proc/" + "PI_processed.csv"
uiProcessedFile = parentdir + "/R2_profiles_HPU_proc/" + "UI_processed.csv"

hiCorrectRecords = 0
uiCorrectRecords = 0
hiNonCorrectRecords = 0
uiNonCorrectRecords = 0
piNonCorrectRecords = 0

class LinkedinSorting():
    def __init__(self):
        #Create the output file header
	self.createOutputFiles(hiProcessedFile)
	self.createOutputFiles(piProcessedFile)
	self.createOutputFiles(uiProcessedFile)
	
    def createOutputFiles(self, filename):
        with open(filename, 'wb') as csvfile:
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
							"PHOTO FILE NAME",
							"PROFESSION_GENERAL_M",
							"PROFESSION_TITLE_M",
							"PROFESSION_SPEC_M",
							"WORKING_STATUS_M",
							"INDUSTRY_M",
							"GEOGRAPHY_M",
							"NON_PROFESSION_M",
							"WORK_LOCATION_M",
							"MATCH" ], 
							delimiter = ';')
	    writer.writeheader()

    def search(self, profileLink, searchFile):
	with open(searchFile, 'r') as doctorfile:
	    rows = unicodecsv.reader(doctorfile, delimiter=';', encoding='utf-8')
	    for row in rows:
		if row[0] == profileLink:
		    return "true"
	return "false"

    def dumpSummary(self):
	f = open(s2dir + 'Summary_processed.txt', 'w+')
	f.write("Number of HI records found in correct file" + ";" + str(hiCorrectRecords))
	f.write("\n")
	f.write("Number of HI records not found in correct file" + ";" + str(hiNonCorrectRecords))
	f.write("\n")
	f.write("Number of PI records not found in correct file" + ";" + str(piNonCorrectRecords))
	f.write("\n")
	f.write("Number of UI records found in correct file" + ";" + str(uiCorrectRecords))
	f.write("\n")
	f.write("Number of UI records not found in correct file" + ";" + str(uiNonCorrectRecords))
	f.write("\n")
	f.close()

    def sort(self, sourceFile, destFile):
	global hiCorrectRecords
	global uiCorrectRecords
	global hiNonCorrectRecords
	global uiNonCorrectRecords
	global piNonCorrectRecords

        with open(sourceFile, 'r') as doctorfile:
	    rows = unicodecsv.reader(doctorfile, delimiter=';', encoding='utf-8')
	    num = 0
	    print rows
	    for row in rows:
		num += 1
		if(num == 1):
		    continue
		name = row[1]
			
		print "Processing profile " + name.encode('utf-8')
	        
		if(self.search(row[6], hiCorrectFile) == "true"): #Write to HI_processed
		    hiCorrectRecords += 1
		    with open(hiProcessedFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[1].encode('utf-8'))
			    el.write("\n")
    	            csvfile.close()
		elif(self.search(row[6], uiCorrectFile) == "true"): #Write to UI_processed
		    uiCorrectRecords += 1
		    with open(uiProcessedFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[1].encode('utf-8'))
			    el.write("\n")
    	            csvfile.close()
		else: #Write to ?_processed
		    if("HI" in destFile):
			hiNonCorrectRecords += 1
		    elif("UI" in destFile):
			uiNonCorrectRecords += 1
		    else:
			piNonCorrectRecords += 1

		    with open(destFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[1].encode('utf-8'))
			    el.write("\n")
    	            csvfile.close()

        
