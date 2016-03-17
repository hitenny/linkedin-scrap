# -*- coding: utf-8 -*-
import csv
import unicodecsv
import unicodedata
import sys
import os
sys.path.append(os.path.abspath('modules'))

import FinalProfileData
from Util import createdirifnotexists,fileexistordie,gettimestamp

nameProfilesMap = {}
nameCountMap = {}
nameInCountMap = {}
profilesAssignmentMap = {
	"NIL"   : 0,
	"YES"   : 0,
	"NO"    : 0,
	"MANUAL": 0,
	"TOTAL" : 0 }

nameAssignmentMap = {
	"NIL"   : 0,
	"YES"   : 0,
	"NO"    : 0,
	"MANUAL": 0,
	"TOTAL" : 0 }

parentdir = "Results_" + gettimestamp()
createdirifnotexists(parentdir)

sumpath = "Summary_" + gettimestamp() + "/S3_YNNM_raw/"
createdirifnotexists(sumpath)

def createOutputCSVFile(filename):
    
    #Create main output file
    with open(filename, 'wb') as csvfile:
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

def createSummaryFile(filename):
    #Create main output file
    with open(filename, 'wb') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = [
							"ASSIGNMENT",
							"#INFILE-NAMES",
							"#LINKEDIN-PROFILES",
							 ], 
							delimiter = ';')
	writer.writeheader()


def addRecordToCSV(plist):
    profilesAssignmentMap["TOTAL"]+=len(plist)

    dirpath = parentdir + "/R3_profiles_YNNM_raw/"
    createdirifnotexists(dirpath)

    for fpd in plist:
	if fpd.profileAssignment == "NIL":
	    profilesAssignmentMap["NIL"]+=1
	    filename = dirpath + "NIL.csv"
	elif fpd.profileAssignment == "NO":
	    profilesAssignmentMap["NO"]+=1
	    filename = dirpath + "NO.csv"
	elif fpd.profileAssignment == "YES":
	    profilesAssignmentMap["YES"]+=1
	    filename = dirpath + "YES_RAW.csv"
	elif fpd.profileAssignment == "MANUAL":
	    profilesAssignmentMap["MANUAL"]+=1
	    filename = dirpath + "MANUAL_RAW.csv"
	for f in [filename, dirpath + "TOTAL.csv"]:
            with open(f, 'ab') as csvfile:
                passi = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8' )	

    	        passi.writerow([fpd.name,
	    				fpd.profileFullName,
	    				fpd.title,
            				fpd.location,
	    				fpd.industry,
            				fpd.li_profile_link,
            				fpd.current_work,
            				fpd.past_work,
            				fpd.num_connections,
            				fpd.summary,
            				fpd.education,
	    				fpd.experience,
	    				fpd.current_title,
            				fpd.skills,
	    				fpd.downloadDate,
	    				fpd.photoPresent,
	    				fpd.photoFileName,
	    				fpd.professionGeneral,
	    				fpd.professionTitle,
	    				fpd.professionSpec,
	    				fpd.workingStatus,
	    				fpd.industryMatch,
	    				fpd.geography,
	    				fpd.nonProfession,
	    				fpd.workLocation,
	    				fpd.match,
					fpd.profileAssignment,
					fpd.numDoctorsInFile,
					str(fpd.numProfiles)])
	    

            csvfile.close()

    nameAssignmentMap["NIL"] = profilesAssignmentMap["NIL"]
    
                
def printData():
    for k in nameProfilesMap:
	print k.encode('utf-8') + "-->" + str(len(nameProfilesMap[k]))

def processData():
    i=0	
    for k in nameProfilesMap:
	profiles = []
	i+=1
	print "Processing profile " + str(i) + " " + k.encode('utf-8')
	for p in nameProfilesMap[k]:
	    profiles.append(p)
	
	profiles = analyzeProfiles(profiles)
	addRecordToCSV(profiles)
    profilesAssignmentMap["TOTAL"] -= profilesAssignmentMap["NIL"]

def analyzeProfiles(profiles):    
    hiMatch = "false"
    piMatch = "false"
    multipleHiMatch = "false"
    multiplePiMatch = "false"
    YesFound = "false"
    NoFound = "false"
    ManualFound = "false"	

    links = []
    #First iteration
    for p in profiles:
	if p.profileFullName == "":
	    continue

	print p.name.encode('utf-8')
	p.numDoctorsInFile = nameInCountMap[p.name.encode('utf-8')]
	
	if p.li_profile_link in links:
	    p.remove = "true"
	if p.li_profile_link != "NIL":
            links.append(p.li_profile_link)

    
    profiles = [ p for p in profiles if p.remove == "false" ]

    numNo = 0
    #Second iteration
    for p in profiles:
	if p.profileFullName != "":  #Profile exists
	    if p.match == "UI":
		p.profileAssignment = "NO"
		numNo += 1

	    if p.match == "PI":
		if piMatch == "true":
		    multiplePiMatch = "true"
		piMatch = "true"

	    if p.match == "HI":
		if hiMatch == "true":
		    multipleHiMatch = "true"
		hiMatch = "true"
	
	    if p.profileAssignment == "NO" and NoFound == "false":
		nameAssignmentMap["NO"] += 1
	  	NoFound = "true";

    
    numManual = 0
    numYes = 0
    
    #Third iteration
    for p in profiles:
	if multipleHiMatch == "true":	#Manual curation required. Mark all HI as MANUAL, PI as NO
	    if p.match == "HI":
		p.profileAssignment = "MANUAL"
		numManual += 1
		
	    if p.match == "PI":
		p.profileAssignment = "NO"
		numNo += 1
	else:
	    if hiMatch == "true":	#Single HI match. Mark HI as YES and rest as NO
		if p.match == "HI":
		    p.profileAssignment = "YES"
		    numYes += 1
		elif p.match == "PI":
		    p.profileAssignment = "NO"
		    numNo += 1			
	    else:
		if multiplePiMatch == "true":
		    if p.match == "PI":
			p.profileAssignment = "MANUAL"
			numManual += 1
		else:
		    if p.match == "PI":
			numYes += 1
		        p.profileAssignment = "YES"

	if p.profileAssignment == "NO" and NoFound == "false":
	    nameAssignmentMap["NO"] += 1
	    NoFound = "true";
	if p.profileAssignment == "YES" and YesFound == "false":
	    nameAssignmentMap["YES"] += 1
	    YesFound = "true";
	if p.profileAssignment == "MANUAL" and ManualFound == "false":
	    nameAssignmentMap["MANUAL"] += 1
	    ManualFound = "true";

    #Third iteration
    for p in profiles:
	if p.profileAssignment == "MANUAL":
	    p.numProfiles = numManual
	if p.profileAssignment == "YES":
	    p.numProfiles = numYes
	if p.profileAssignment == "NO":
	    p.numProfiles = numNo


    return profiles
	
def loadInputData():	
    #Load input files
    with open('infiles/doctors.csv', 'r') as infile:
	rows = unicodecsv.reader(infile, delimiter=',', encoding='ISO-8859-1')
        for row in rows:
	    name = (row[2] + " " + row[1]).encode('utf-8')
	    if name in nameInCountMap:
	        nameInCountMap[name] += 1
	    else:
		print name
		nameInCountMap[name] = 1

    infile = parentdir + "/R1_profiles_HPU_raw/" + "ALL-RECORDS.csv"
    with open(infile, 'r') as profilefile:
	rows = unicodecsv.reader(profilefile, delimiter=';', encoding='utf-8')
	
        for row in rows:
	    if row[1] == "NAME":
	        continue

	    fpd = FinalProfileData.FinalProfileData()
	    
	    print row[2].encode('utf-8')
	    fpd.name = row[1]
	    fpd.profileFullName = row[2]
	    fpd.title = row[3]
            fpd.location = row[4]
	    fpd.industry = row[5]
            fpd.li_profile_link = row[6]
            fpd.current_work = row[7]
            fpd.past_work = row[8]
            fpd.num_connections = row[9]
            fpd.summary = row[10]
            fpd.education = row[11]
	    fpd.experience = row[12]
	    fpd.current_title = row[13]
            fpd.skills = row[14]
	    fpd.downloadDate = row[15]
	    fpd.photoPresent = row[16]
	    fpd.photoFileName = row[17]
	    fpd.professionGeneral = row[18]
	    fpd.professionTitle = row[19]
	    fpd.professionSpec = row[20]
	    fpd.workingStatus = row[21]
	    fpd.industryMatch = row[22]
	    fpd.geography = row[23]
	    fpd.nonProfession = row[24]
	    fpd.workLocation = row[25]
	    fpd.match = row[26]
	
	    if row[1] in nameProfilesMap:
	        nameProfilesMap[row[1]].append(fpd)
	    else:
		nameProfilesMap[row[1]] = [fpd]

	    if row[1] in nameCountMap:
	        nameCountMap[row[1]] += 1
	    else:
		nameCountMap[row[1]] = 1    

def printSummary():
    nameAssignmentMap["TOTAL"] = nameAssignmentMap["NO"] + nameAssignmentMap["MANUAL"] + nameAssignmentMap["YES"]+ nameAssignmentMap["NIL"]
    
    dirpath = parentdir + "/R3_profiles_YNNM_raw/"
    createdirifnotexists(dirpath)

    f = open(sumpath + "summary.csv", 'ab')
    f.write("NIL;" + str(nameAssignmentMap["NIL"]) + ";0\n")
    f.write("YES;" + str(nameAssignmentMap["YES"]) + ";" + str(profilesAssignmentMap["YES"]) + "\n")
    f.write("NO;" + str(nameAssignmentMap["NO"]) + ";" + str(profilesAssignmentMap["NO"]) + "\n")
    f.write("MANUAL;" + str(nameAssignmentMap["MANUAL"]) + ";" + str(profilesAssignmentMap["MANUAL"]) + "\n")
    f.write("TOTAL;" + str(nameAssignmentMap["TOTAL"]) + ";" + str(profilesAssignmentMap["TOTAL"]) + "\n")
    f.close()

if __name__ == "__main__":
    loadInputData()
    
    createdirifnotexists(parentdir)

    dirpath = parentdir + "/R3_profiles_YNNM_raw/"
    createdirifnotexists(dirpath)
    
    createOutputCSVFile(dirpath + "NIL.csv")
    createOutputCSVFile(dirpath + "YES_RAW.csv")
    createOutputCSVFile(dirpath + "NO.csv")
    createOutputCSVFile(dirpath + "MANUAL_RAW.csv")
    createOutputCSVFile(dirpath + "TOTAL.csv")
    createSummaryFile(sumpath + "summary.csv")
    
    processData()
    printSummary();
    	
    

	
	
    
