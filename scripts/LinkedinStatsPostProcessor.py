# -*- coding: utf-8 -*-
import csv
import unicodecsv
import unicodedata
import shutil
import sys
import os
sys.path.append(os.path.abspath('modules'))

from Util import createdirifnotexists,fileexistordie,gettimestamp

manual_ignore_list = []
yes_ignore_list = []
verified_list = []

parentdir = "Results_" + gettimestamp()
createdirifnotexists(parentdir)

processeddir = parentdir + "/R4_profiles_YNNM_proc/"
verifieddir = parentdir + "/R5_final_proc/"
createdirifnotexists(processeddir)
createdirifnotexists(verifieddir)

summarypath = "Summary_" + gettimestamp()
createdirifnotexists(summarypath)
s4dir = summarypath + "/S4_YNNM_PROC/"
createdirifnotexists(s4dir)
s5dir = summarypath + "/S5_final_proc/"
createdirifnotexists(s5dir)

#Summary data
manualIgnoreRecords = 0
yesIgnoreRecords = 0
manualProcessedRecords = 0
yesProcessedRecords = 0
manualVerified = 0
yesVerified = 0
manualUnVerified = 0
yesUnVerified = 0

def createOutputCSVFile(filename):
    
    #Create main output file
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
							"MATCH",
							"PROFILE ASSIGNMENT",
							"NUMBER OF DOCTORS",
							"#LINKEDIN PROFILES"
							 ], 
							delimiter = ';')
	writer.writeheader()
                
def processData():
    global manualIgnoreRecords
    global yesIgnoreRecords
    global manualProcessedRecords		
    global yesProcessedRecords		
    	
    dirpath = parentdir + "/R3_profiles_YNNM_raw/" 
    with open(dirpath + 'MANUAL_RAW.csv', 'r') as infile, open(processeddir + 'MANUAL_PROCESSED.csv', 'ab') as outfile:
	rows = unicodecsv.reader(infile, delimiter=';', encoding='utf-8')
	writer = unicodecsv.writer(outfile, delimiter=';', encoding='utf-8')
	for row in rows:
	    if(row[6] in manual_ignore_list): #Ignore it
		manualIgnoreRecords += 1
		continue
	    else:
		manualProcessedRecords += 1
		writer.writerow(row)

    with open(dirpath + 'YES_RAW.csv', 'r') as infile, open(processeddir + 'YES_PROCESSED.csv', 'ab') as outfile:
	rows = unicodecsv.reader(infile, delimiter=';', encoding='utf-8')
	writer = unicodecsv.writer(outfile, delimiter=';', encoding='utf-8')	
	for row in rows:
	    if(row[6] in yes_ignore_list): #Ignore it	
		yesIgnoreRecords += 1
		continue
	    else:
		yesProcessedRecords
		writer.writerow(row)

def processVerifiedData():
    global yesVerified
    global manualVerified
    global yesUnVerified
    global manualUnVerified

    with open(processeddir + 'YES_PROCESSED.csv', 'r') as infile, open(verifieddir + 'YES_VERIFIED.csv', 'ab') as yesvfile, open(verifieddir + 'YES_UNVERIFIED.csv', 'ab') as yesuvfile:
	rows = unicodecsv.reader(infile, delimiter=';', encoding='utf-8')
	vwriter = unicodecsv.writer(yesvfile, delimiter=';', encoding='utf-8')
	uvwriter = unicodecsv.writer(yesuvfile, delimiter=';', encoding='utf-8')
	for row in rows:
	    dr_linkedin_id = row[0] + "-" + row[6]
	    if(dr_linkedin_id in verified_list): 
		vwriter.writerow(row)
		yesVerified += 1
	    else:
		yesUnVerified += 1
		uvwriter.writerow(row)

    with open(processeddir + 'MANUAL_PROCESSED.csv', 'r') as infile, open(verifieddir + 'MANUAL_VERIFIED.csv', 'ab') as manualvfile, open(verifieddir + 'MANUAL_UNVERIFIED.csv', 'ab') as manualuvfile:
	rows = unicodecsv.reader(infile, delimiter=';', encoding='utf-8')
	vwriter = unicodecsv.writer(manualvfile, delimiter=';', encoding='utf-8')
	uvwriter = unicodecsv.writer(manualuvfile, delimiter=';', encoding='utf-8')		
	for row in rows:
	    dr_linkedin_id = row[0] + "-" + row[6]
	    if(dr_linkedin_id in verified_list): 	
		vwriter.writerow(row)
		manualVerified += 1
	    else:
		manualUnVerified += 1
		uvwriter.writerow(row)

    #Merge YES_VERIFIED.csv and MANUAL_VERIFIED.csv into linkedinDr.csv 
    with open(verifieddir + 'YES_VERIFIED.csv', 'ab') as yesvfile, open(verifieddir + 'linkedinDr.csv', 'ab') as drfile:
        rows = unicodecsv.reader(yesvfile, delimiter=';', encoding='utf-8')
        for row in rows:
	    drfile.writerow(row)

    with open(verifieddir + 'MANUAL_VERIFIED.csv', 'r') as manvfile, open(verifieddir + 'linkedinDr.csv', 'ab') as drfile:
        rows = unicodecsv.reader(manvfile, delimiter=';', encoding='utf-8')
        for row in rows:
	    drfile.writerow(row)

	
def loadIgnoreData():	
    #Load input files
    configdir = "Config_" + gettimestamp()
    manualignorefile = configdir + "/C3_YNNM_raw/" + 'MANUAL_IGNORE-LIST.csv'
    yesignorefile = configdir + "/C3_YNNM_raw/" + 'YES_IGNORE-LIST.csv'  

    fileexistordie(manualignorefile)
    fileexistordie(yesignorefile)

    infile = open(manualignorefile, 'r')
    for row in infile:
	manual_ignore_list.append(row.strip())

    f = open(yesignorefile, 'r')
    for row in f:
	yes_ignore_list.append(row.strip())

def loadVerifiedData():	
    #Load input files
    configdir = "Config_" + gettimestamp()
    verifiedfile = configdir + "/C3_YNNM_proc/" + 'MainDrID-LinkedInID_verified_map.csv' 
    fileexistordie(verifiedfile)

    infile = open(verifiedfile, 'r')
    for row in infile:
	verified_list.append(row.strip())


def copyPhotos():
    with open(verifieddir + '/linkedinDr.csv', 'r') as drfile:
        rows = unicodecsv.reader(drfile, delimiter=';', encoding='utf-8')
	for row in rows:
	    if row[1] == "NAME":
		continue
	    picfilename = row[17]
	    shutil.copy2('photos/' + picfilename, 'LinkedInDr_Photos/' + picfilename) 
	    
def dumpSummary():
    f = open(s4dir + 'Summary_YNNM_processed.txt', 'w+')
    f.write("Number of YES records ignored" + ";" + str(yesIgnoreRecords))
    f.write("\n")
    f.write("Number of MANUAL records ignored" + ";" + str(manualIgnoreRecords))
    f.write("\n")
    f.write("Number of YES records processed" + ";" + str(yesProcessedRecords))
    f.write("\n")
    f.write("Number of MANUAL records processed" + ";" + str(manualProcessedRecords))
    f.write("\n")

    f = open(s5dir + 'Summary_final_proc.txt', 'w+')
    f.write("Number of YES records verified" + ";" + str(yesVerified))
    f.write("\n")	
    f.write("Number of MANUAL records verified" + ";" + str(yesVerified))
    f.write("\n")	
    f.write("Number of YES records unverified" + ";" + str(yesUnVerified))
    f.write("\n")	
    f.write("Number of MANUAL records unverified" + ";" + str(manualUnVerified))
    f.write("\n")	

if __name__ == "__main__":
    loadIgnoreData()
    loadVerifiedData()

    createOutputCSVFile(processeddir + "/MANUAL_PROCESSED.csv")
    createOutputCSVFile(processeddir + "/YES_PROCESSED.csv")
    
    processData() #It creates *PROCESSED files

    createOutputCSVFile(verifieddir + "/MANUAL_VERIFIED.csv")
    createOutputCSVFile(verifieddir + "/YES_VERIFIED.csv")
    createOutputCSVFile(verifieddir + "/MANUAL_UNVERIFIED.csv")
    createOutputCSVFile(verifieddir + "/YES_UNVERIFIED.csv")
    createOutputCSVFile(verifieddir + "/linkedinDr.csv")
    
    copyPhotos() #Copy photos of LinkedInDr_Photos
    dumpSummary()
    	
    

	
	
    
