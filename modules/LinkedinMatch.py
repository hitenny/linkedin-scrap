# -*- coding: utf-8 -*-
import csv
import os
import re
import unicodecsv
import unicodedata
import KeywordFileReader
import Kwstats
from Util import createdirifnotexists,fileexistordie,gettimestamp

KW_PROFESSION_GENERAL_MATCHES = {}
KW_PROFESSION_TITLE_MATCHES = {}
KW_PROFESSION_SPEC_MATCHES = {}
KW_WORKING_STATUS_MATCHES = {}
KW_INDUSTRY_M_MATCHES = {}
KW_GEOGRAPHY_M_MATCHES = {}
KW_NON_PROFESSION_MATCHES = {}
KW_WORK_LOCATION_MATCHES = {}

UNIQUE_PROFILES = []

parentdir = "Results_" + gettimestamp()
createdirifnotexists(parentdir)
    
summarypath = "Summary_" + gettimestamp()
createdirifnotexists(summarypath)

rawdir = parentdir + "/R1_profiles_HPU_raw/"
createdirifnotexists(rawdir)

s1dir = summarypath + "/S1_KW/"
createdirifnotexists(s1dir)

allFile = rawdir + "ALL-RECORDS.csv"
hiFile = rawdir + "HI_raw.csv"
piFile = rawdir + "PI_raw.csv"
uiFile = rawdir + "UI_raw.csv"

class LinkedinMatch():
    def __init__(self):
        #Create the output file header
	self.createOutputFiles(allFile)
	self.createOutputFiles(hiFile)
	self.createOutputFiles(piFile)
	self.createOutputFiles(uiFile)
	    			
	#Create keyword out files
	f = open(summarypath + "/S1_KW/" + 'KW_Profession_general.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Profession_title.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Profession_spec.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Working_status.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Industry_M.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Geography_M.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_non-profession_titles.txt', 'w')
	f = open(summarypath + "/S1_KW/" + 'KW_Working_place.txt', 'w')

	#Create stats file
	f = open(summarypath + "/S1_KW/" + '/kwstats.txt', 'w')

	for kw in KeywordFileReader.KW_PROFESSION_GENERAL:
	    KW_PROFESSION_GENERAL_MATCHES[kw] = 0
	
	for kw in KeywordFileReader.KW_PROFESSION_TITLE:
	    KW_PROFESSION_TITLE_MATCHES[kw] = 0

	for kw in KeywordFileReader.KW_PROFESSION_SPEC:
	    KW_PROFESSION_SPEC_MATCHES[kw] = 0
	
	for kw in KeywordFileReader.KW_WORKING_STATUS:
	    KW_WORKING_STATUS_MATCHES[kw] = 0
	
	for kw in KeywordFileReader.KW_INDUSTRY_M:
	    KW_INDUSTRY_M_MATCHES[kw] = 0

	for kw in KeywordFileReader.KW_GEOGRAPHY_M:
	    KW_GEOGRAPHY_M_MATCHES[kw] = 0

	for kw in KeywordFileReader.KW_NON_PROFESSION:
	    KW_NON_PROFESSION_MATCHES[kw] = 0	

	for kw in KeywordFileReader.KW_WORK_LOCATION:
	    KW_WORK_LOCATION_MATCHES[kw] = 0
	
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


    def printRow(self,row):
        print "NAME:" + row[1].encode('utf-8') + "\n"
	print "PROFILE NAME:" + row[2].encode('utf-8') + "\n"
	print "TITLE:" + row[3].encode('utf-8') + "\n"
	print "LOCATION:" + row[4].encode('utf-8') + "\n" 
	print "INDUSTRY:" + row[5].encode('utf-8') + "\n"
	print "PUBLIC PROFILE LINK:" + row[6].encode('utf-8') + "\n" 
	print "CURRENT WORK:" + row[7].encode('utf-8') + "\n"
	print "PAST WORK:" + row[8].encode('utf-8') + "\n"
	print "CONNECTIONS:" + row[9].encode('utf-8') + "\n"
	print "SUMMARY:" + row[10].encode('utf-8') + "\n"	
	print "EDUCATION:" + row[11].encode('utf-8') + "\n"
	print "EXPERIENCE:" + row[12].encode('utf-8') + "\n"
	print "CURRENT TITLE:" + row[13].encode('utf-8') + "\n"
	print "SKILLS:" + row[14].encode('utf-8') + "\n"
	print "DOWNLOAD DATE:" + row[15].encode('utf-8') + "\n"
	print "PHOTO PRESENT:" + row[16].encode('utf-8') + "\n"
	print "PHOTO FILE NAME:" + row[17].encode('utf-8') + "\n"

    def match(self):
        first_run = "false"
		
	k = Kwstats.Kwstats()
	el = open(summarypath + "/S1_KW/" + 'error.csv', 'w')
	infile = parentdir + "/R0_profiles_raw/" + "profiles-final.csv"
        with open(infile, 'r') as doctorfile:
	    rows = unicodecsv.reader(doctorfile, delimiter=';', encoding='utf-8')
	
	    num_processed = 0
	    for row in rows:
		#print row
	        if(num_processed == 0):
	            num_processed = 1
	            continue	

	        name = row[1]
	
		if(row[6] in UNIQUE_PROFILES):
		    continue
		else:
	   	    UNIQUE_PROFILES.append(row[6])
		
		print "Processing profile [" + str(num_processed) + "] . Matching " + name.encode('utf-8')
	        ret1 = self.match_prof_general(row)
		row.append(ret1)
	        if(ret1 != "NIL"):
		    k.KW_hits["KW_PROFESSION_GENERAL"] += 1

	        ret2 = self.match_prof_title(row)
		row.append(ret2)
	        if(ret2 != "NIL"):
		    k.KW_hits["KW_PROFESSION_TITLE"] += 1
 
	        ret3 = self.match_prof_spec(row)
	        row.append(ret3)
	        if(ret3 != "NIL"):
		    k.KW_hits["KW_PROFESSION_SPEC"] += 1

	        ret4 = self.match_working_status(row)	
	        row.append(ret4)
	        if(ret4 != "NIL"):
		    k.KW_hits["KW_WORKING_STATUS"] += 1

	        ret5 = self.match_industry(row)
	        row.append(ret5)
	        if(ret5 != "NIL"):
		    k.KW_hits["KW_INDUSTRY_M"] += 1

	        ret6 = self.match_geography(row)
	        row.append(ret6)
	        if(ret6 != "NIL"):
		    k.KW_hits["KW_GEOGRAPHY_M"] += 1
	    
	        ret7 = self.match_non_prof_title(row)	
	        row.append(ret7)
	        if(ret7 != "NIL"):
		    k.KW_hits["KW_NON_PROFESSION"] += 1

	        ret8 = self.match_work_location(row)
                row.append(ret8)
	        if(ret8 != "NIL"):
		    k.KW_hits["KW_WORK_LOCATION"] += 1

	        if(ret1 != "NIL" or ret2 != "NIL" or ret3 != "NIL"):
		    k.KW_high_interest_hits += 1
		    row.append("HI")
		    with open(hiFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[1].encode('utf-8'))
			    el.write("\n")
    	            csvfile.close()	

	        if(ret5 != "NIL" and ret1 == "NIL" and ret2 == "NIL" and ret3 == "NIL" and ret7 == "NIL"):
		    k.KW_possible_interest_hits += 1
		    row.append("PI")
		    with open(piFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[1].encode('utf-8'))
			    el.write("\n")
    	            csvfile.close()	
	
		ui = "false"
	        if(ret5 == "NIL" and ret1 == "NIL" and ret2 == "NIL" and ret3 == "NIL"):
		    k.KW_uninterest_1_hits += 1
		    row.append("UI")
		    ui = "true"	
		    with open(uiFile, 'ab') as csvfile:
    	                try:
		            writer = unicodecsv.writer(csvfile, delimiter=';')	
		            writer.writerow(row)
		        except UnicodeDecodeError:
			    print "Error while printing record"
			    el.write(row[2].encode('utf-8'))
			    el.write("\n")
    	                csvfile.close()	


	        if(ret1 == "NIL" and ret2 == "NIL" and ret3 == "NIL" and ret5 != "NIL" and ret7 != "NIL"):
		    k.KW_uninterest_2_hits += 1
		    if ui == "false":
			row.append("UI")
			with open(uiFile, 'ab') as csvfile:
    	                    try:
		                writer = unicodecsv.writer(csvfile, delimiter=';')	
		                writer.writerow(row)
		            except UnicodeDecodeError:
			        print "Error while printing record"
			        el.write(row[2].encode('utf-8'))
			        el.write("\n")
    	                csvfile.close()	
 

		
	        with open(allFile, 'ab') as csvfile:
    	            try:
		        writer = unicodecsv.writer(csvfile, delimiter=';')	
		        writer.writerow(row)
		    except UnicodeDecodeError:
			print "Error while printing record"
			el.write(row[2].encode('utf-8'))
			el.write("\n")
    	        csvfile.close()

	        num_processed = num_processed + 1
	
	self.dumpStats(k, num_processed)
	
    def dumpStats(self, stats, num):
	f = open(summarypath + "/S1_KW/" + 'KW_Profession_general.txt', 'w+')
	for k in KeywordFileReader.KW_PROFESSION_GENERAL:
	    f.write(k + ";" + str(KW_PROFESSION_GENERAL_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_Profession_title.txt', 'w+')
	for k in KeywordFileReader.KW_PROFESSION_TITLE:
	    f.write(k + ";" + str(KW_PROFESSION_TITLE_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_Profession_spec.txt', 'w+')
	for k in KeywordFileReader.KW_PROFESSION_SPEC:
	    f.write(k + ";" + str(KW_PROFESSION_SPEC_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_Working_status.txt', 'w+')
	for k in KeywordFileReader.KW_WORKING_STATUS:
	    f.write(k + ";" + str(KW_WORKING_STATUS_MATCHES[k]))
	    f.write("\n")
	f.close()
	
	f = open(summarypath + "/S1_KW/" + 'KW_Industry_M.txt', 'w+')
	for k in KeywordFileReader.KW_INDUSTRY_M:
	    f.write(k + ";" + str(KW_INDUSTRY_M_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_Geography_M.txt', 'w+')
	for k in KeywordFileReader.KW_GEOGRAPHY_M:
	    f.write(k + ";" + str(KW_GEOGRAPHY_M_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_non-profession_titles.txt', 'w+')
	for k in KeywordFileReader.KW_NON_PROFESSION:
	    f.write(k + ";" + str(KW_NON_PROFESSION_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'KW_Working_place.txt', 'w+')
	for k in KeywordFileReader.KW_WORK_LOCATION:
	    f.write(k + ";" + str(KW_WORK_LOCATION_MATCHES[k]))
	    f.write("\n")
	f.close()

	f = open(summarypath + "/S1_KW/" + 'kwstats.txt', 'w+')
	f.write("[MAIN CATEGORIES]\n")
	f.write("#Linkedin profiles:" + str(num-1) + "\n" )
	f.write("#profiles w hit in PROFESSION_GENERAL:" + str(stats.KW_hits["KW_PROFESSION_GENERAL"]) + "\n")
	f.write("#profiles w hit in PROFESSION_TITLE:" + str(stats.KW_hits["KW_PROFESSION_TITLE"]) + "\n")
	f.write("#profiles w hit in PROFESSION_SPEC:" + str(stats.KW_hits["KW_PROFESSION_SPEC"]) + "\n")
	f.write("#profiles w hit in INDUSTRY_M:" + str(stats.KW_hits["KW_INDUSTRY_M"]) + "\n")
	f.write("#profiles w hit in GEOGRAPHY_M:" + str(stats.KW_hits["KW_GEOGRAPHY_M"]) + "\n")
	f.write("#profiles w hit in NON-PREFESSION:" + str(stats.KW_hits["KW_NON_PROFESSION"]) + "\n")
	f.write("#profiles w hit in WORKING STATUS:" + str(stats.KW_hits["KW_WORKING_STATUS"]) + "\n\n")

	f.write("[HIGHLY INTERESTING]\n")
	f.write("#profiles w hit in G, T or S :" + str(stats.KW_high_interest_hits) + "\n\n")
	f.write("[POSSIBLY INTERESTING]\n")
	f.write("#profiles wo hit in (G, T or S) and w hit in (I) and wo hit in N-P:" + str(stats.KW_possible_interest_hits) + "\n\n")
	f.write("[UN-INTERESTING]\n")
	f.write("#profiles wo hit in (G, T or S) and wo hit in (I):" + str(stats.KW_uninterest_1_hits) + "\n")
	f.write("#profiles wo hit in (G, T or S) and w hit in (I) and N-P:" + str(stats.KW_uninterest_2_hits) + "\n")

    def matchpattern(self, pattern, string):
	match_pattern = ""
	if(pattern.find('*') > -1): #substring search
	    if(pattern.find('*') == 0 and pattern.find('*') == len(pattern)-1):
		pattern = pattern.replace('*','')
	        regpattern = r'(\S*' + re.escape(pattern) + r'\S*)'
	        r = re.search(regpattern,string,re.UNICODE|re.IGNORECASE)
	        try:
		    match_pattern = r.group()
	        except AttributeError:
		    match_pattern = ""
	    elif(pattern.find('*') == 0): #*pattern
		pattern = pattern.replace('*','')
		regpattern = r'(\S*' + re.escape(pattern) + r'\b)'
	        r = re.search(regpattern,string,re.UNICODE|re.I)
	        try:
		    match_pattern = r.group()
	        except AttributeError:
		    match_pattern = ""
	    elif(pattern.find('*') == len(pattern)-1): #pattern*
		pattern = pattern.replace('*','')
	        regpattern = r'(\b' + re.escape(pattern) + r'\S*)'
	        r = re.search(regpattern,string,re.UNICODE|re.IGNORECASE)
	        try:
		    match_pattern = r.group()
		except AttributeError:
		    match_pattern = ""
	else:
	    regpattern = r'(\b' + re.escape(pattern) + r'\b)'
	    r = re.search(regpattern,string,re.UNICODE|re.IGNORECASE)
	    try:
		match_pattern = r.group()
	    except AttributeError:
		match_pattern = ""

	return match_pattern


    def match_prof_general(self,record): 
	summary = record[2] + " " + record[3] + " " + record[12]
	match_patterns = ""
	for kw in KeywordFileReader.KW_PROFESSION_GENERAL:
	    x = self.matchpattern(kw, summary.encode('utf-8'))
	    if(x != ""):
		print x + " matched \n"
		match_patterns = match_patterns + x + "|"
		KW_PROFESSION_GENERAL_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"

	return match_patterns
		           
    def match_prof_title(self, record):
	summary = record[3] + " " + record[12]
	match_patterns = ""
  	for kw in KeywordFileReader.KW_PROFESSION_TITLE:
	    x = self.matchpattern(kw, summary.encode('utf-8'))
	    if (x != ""):
		print kw + " matched\n with string:" + x
		match_patterns = match_patterns + x + "|"
		KW_PROFESSION_TITLE_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_prof_spec(self, record):
	summary = record[3] + " " + record[12]
	match_patterns = ""
  	for kw in KeywordFileReader.KW_PROFESSION_SPEC:
	    x = self.matchpattern(kw, summary.encode('utf-8'))
	    if (x!= ""):
		print kw + " matched with string:" + x + "\n"
		match_patterns = match_patterns + x + "|"
		KW_PROFESSION_SPEC_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_working_status(self, record):
	summary = record[3] + " " + record[12]
	match_patterns = ""
  	for kw in KeywordFileReader.KW_WORKING_STATUS:
	    x = self.matchpattern(kw, summary.encode('utf-8'))
	    if(x!= ""):
		print x + " matched\n"
		match_patterns = match_patterns + x + "|"
		KW_WORKING_STATUS_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_industry(self, record):
	industry = record[5]
	
	match_patterns = ""
  	for kw in KeywordFileReader.KW_INDUSTRY_M:
	    x = self.matchpattern(kw, industry.encode('utf-8'))
	    if(x!= ""):
		print x + " matched\n"
		match_patterns = match_patterns + x + "|"
		KW_INDUSTRY_M_MATCHES[kw] = KW_INDUSTRY_M_MATCHES[kw]+1 if kw in KW_INDUSTRY_M_MATCHES else 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_geography(self, record):
	geography = record[4]
	match_patterns = ""
	print "Geography:" + geography.encode('utf-8')
  	for kw in KeywordFileReader.KW_GEOGRAPHY_M:
	    x = self.matchpattern(kw, geography.encode('utf-8'))
	    if (x!=""):
		print x + " matched\n"
		match_patterns = match_patterns + x + "|"
		KW_GEOGRAPHY_M_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_non_prof_title(self, record):
	summary = record[3] + " " + record[12]
	match_patterns = ""
  	for kw in KeywordFileReader.KW_NON_PROFESSION:
	    x = self.matchpattern(kw, summary.encode('utf-8')) 
	    if(x!=""):
		print x + " matched\n"
		match_patterns = match_patterns + x + "|"
		KW_NON_PROFESSION_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns

    def match_work_location(self, record):
	location = record[4]
	print "\n\nLocation:" + location.encode('utf-8')
	match_patterns = ""
  	for kw in KeywordFileReader.KW_WORK_LOCATION:
	    x = self.matchpattern(kw, location.encode('utf-8'))	
	    if(x!=""):
		print x + " matched\n"
		match_patterns = match_patterns + x + "|"
		KW_WORK_LOCATION_MATCHES[kw] += 1
		
	if match_patterns == "":
	    match_patterns = "NIL"
 
	return match_patterns
    
