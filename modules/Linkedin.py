# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from datetime import date
import unittest, time, re
import csv
import unicodecsv
import urllib
from Util import createdirifnotexists,fileexistordie,gettimestamp
import sys
import os
sys.path.append(os.path.abspath('modules'))
import ProfileData

parentdir = ""

photosdir = "photos_" + gettimestamp()
createdirifnotexists(photosdir)

sumpath = "Summary_" + gettimestamp() + "/S0_raw/"
createdirifnotexists(sumpath)

#Summary data
numSearches = 0
noMatches = 0
exactMatches = 0
multipleMatches = 0

class LinkedinDownload(unittest.TestCase):
    def __init__(self):
	self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)
        self.base_url = "https://se.linkedin.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
	
	self.driver.get(self.base_url)

    def checkElementExists(self, path):
        try:
	    self.driver.find_element_by_xpath(path)
	except NoSuchElementException:
	    return False
	return True
	            
    def search(self, first_name, last_name, reqId, outDir):
	    global parentdir
	    parentdir = outDir
	    name = first_name + " " + last_name
	    if(not name.strip()):
		return
		
	    searchUrl = self.base_url + "/pub/dir/?first=" + first_name + "&last=" + last_name + "&search=Search" 
	    self.searchPeople(name, searchUrl, reqId)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
    	
    def dumpSummary(self):
	f = open(sumpath + "summary_scrap.csv", 'ab')
        f.write("Number of profiles searches;" + str(numSearches) + "\n")
	f.write("Number of No matches;" + str(noMatches) + "\n")
	f.write("Number of exact matches;" + str(exactMatches) + "\n")
	f.write("Number of multiple matches;" + str(multipleMatches) + "\n")
    
    def searchPeople(self, user, searchUrl, reqId):
	global numSearches
        global noMatches
	global exactMatches
	global multipleMatches

	numSearches += 1

	self.driver.get(searchUrl)

	no_profile = ProfileData.ProfileData()
        no_profile.name = user
	no_profile.reqId = reqId
	no_profile_list = []	
	no_profile_list.append(no_profile)

	#We will be in profile page in case of exact match and single result
	try:	        
	    topCard = self.driver.find_element_by_xpath("//section[@id='topcard']")
	except NoSuchElementException:
	    try:
		resultset = self.driver.find_element_by_xpath("//div[@class='primary-section']")
	    except NoSuchElementException:
	        print("There are no matches")
		noMatches += 1
		self.addRecordToCSV(no_profile_list)
	    else:
		multipleMatches += 1
		print("There are multiple name matches")
		self.downloadProfiles(user, searchUrl, reqId)	
	else:
	    exactMatches += 1
	    print("There is exact name match")
	    self.scrapProfilePage(user, "true", reqId)
	        
	
    def scrapProfilePage(self, name, match, reqId):
	profile_list = []
	proceed = 0
	
	self.profileData = ProfileData.ProfileData()
	self.profileData.name = name
	self.profileData.reqId = reqId
	
	#Public profile link	
        pub_profile = self.driver.current_url
	x = pub_profile.find("?")
	if(x > 0):
	    self.profileData.li_profile_link = pub_profile[0:pub_profile.find("?")]
	else:
	    self.profileData.li_profile_link = pub_profile
    
	try:	        
	    topCard = self.driver.find_element_by_xpath("//section[@id='topcard']")
	except NoSuchElementException:
	    print("Top card not found")
	else:
	    try:
		#Title
		profile_overview = topCard.find_element_by_xpath("//div[@class='profile-overview']")
		self.profileData.title = profile_overview.find_element_by_xpath("//p[contains(@class, 'title')]").text
	    except NoSuchElementException:
		print("Title not found")

	    try:
		#Name
		self.profileData.profileFullName = profile_overview.find_element_by_xpath("//h1[@id='name']").text
	    except NoSuchElementException:
		print("Full name not found")
	
	    industry = ""	
	    try:
		#Location/Industry
		self.profileData.location = profile_overview.find_element_by_xpath("//span[@class='locality']").text
		self.profileData.industry = profile_overview.find_element_by_xpath("//dd[@class='descriptor']").text
	    except NoSuchElementException:
		print("Location not found")

		#Profile picture
	    try:
		profile_pic = topCard.find_element_by_xpath("//div[@class='profile-picture']")
		picUrl = profile_pic.find_element_by_xpath("//a/img").get_attribute('src')
		r = str(time.time())
		randomnum = r[0:r.find(".")][-3:]
		if "ghost" in picUrl:
		    self.profileData.photoPresent = "N"
		else:
		    picfilename = self.profileData.profileFullName.encode('ascii','ignore')
		    picfilename = picfilename.replace(" ","").replace(":","").replace("/","").replace("\\","").replace(",","").replace(".","").replace("\"","").replace("'","").replace("|","") + randomnum + ".jpg"
		    self.profileData.photoFileName = picfilename
		    urllib.urlretrieve(picUrl, photosdir + "/" + picfilename)
		    self.profileData.photoPresent = "Y"
		    
	    except NoSuchElementException:
		self.profileData.photoPresent = "N"
		print ("Photo not present")

	    try:
		#Current work	
	        current = profile_overview.find_element_by_xpath("//tr[@data-section='currentPositions']/td/ol") 
		items = current.find_elements_by_tag_name("li")
		for item in items:
		    try:
		        curitem = item.find_element_by_xpath(".//span[@class='org']").text
		    except NoSuchElementException:
			curitem = item.find_element_by_xpath(".//span").text

		    self.profileData.current_work = self.profileData.current_work + curitem + ","
	    except NoSuchElementException:
		print("Current work not found")
	
	    try:
		#Past work
		past = profile_overview.find_element_by_xpath("//tr[@data-section='pastPositions']/td/ol") 
		items = past.find_elements_by_tag_name("li")
		for item in items:
		    self.profileData.past_work = self.profileData.past_work + item.text + " "
 	    except NoSuchElementException:
		print("Past work not found")

	    try:	
		#Education
		self.profileData.education = profile_overview.find_element_by_xpath("//tr[@data-section='educations']/td/ol/li").text 
	    except NoSuchElementException:
		print("Education not found")	

	    try:
		#Connections
		self.profileData.num_connections = profile_overview.find_element_by_xpath("//div[contains(@class, 'member-connections')]/strong").text
		self.profileData.num_connections = re.sub("[^0-9]", "", self.profileData.num_connections) #Remove non-numerics from connections For eg, 500+

	    except NoSuchElementException:
		print("Connections not found")


	try:	
	#Experience
	    experience = self.driver.find_element_by_xpath("//section[@id='experience']/ul")
	    explist = experience.find_elements_by_tag_name("li")
	    for e in explist:
		try:
		    title = e.find_element_by_class_name("item-title").text
		    try:
		        company = e.find_element_by_class_name("item-subtitle").text
		    except NoSuchElementException:
			print "Company not found"
		    
		    date_range = e.find_element_by_class_name("date-range")
                    speriod = date_range.find_element_by_xpath(".//time[1]").text
		    try:
			eperiod = e.find_element_by_xpath(".//time[2]").text
		    except NoSuchElementException:
			eperiod = "Present"
		except NoSuchElementException:
		    print "No element"
		    continue
		
 		exp = "Title:" + title.encode("utf-8") + "|" + "Company:" + company.encode("utf-8") + "|" + "Duration:" + speriod.encode("utf-8") + "-" + eperiod.encode("utf-8")
		self.profileData.experience.append(exp)
	except NoSuchElementException:
	    print("Experience not found")	

	if(len(self.profileData.experience) > 0):
	    x = self.profileData.experience[0]
	    self.profileData.current_title = x[x.find(":")+1: x.find("|")];

	    
	try:
	    skillsSection = self.driver.find_element_by_xpath("//section[@id='skills']/ul") 
	except NoSuchElementException:
	    print ("Skills section not found")
	else:
	    try:
		#Skills
	        skills = skillsSection.find_elements_by_tag_name("li")
		for s in skills:
		    try:
		        skill = s.find_element_by_xpath(".//a/span").text
		        self.profileData.skills.append( skill)
	    	    except NoSuchElementException:
	    	        break
	    except NoSuchElementException:
	        print("Skill section not found")

	try:
	#Summary
	    summarySection = self.driver.find_element_by_xpath("//section[@id='summary']") 
	    self.profileData.summary = summarySection.find_element_by_xpath("//div[@class='description']").text
	   
	except NoSuchElementException:
	    print("Summary section not found")
	
	if(match == "true"):
	    self.profileData.downloadDate = str(date.today())	
	    profile_list.append(self.profileData)
	    self.addRecordToCSV(profile_list)
	
	return self.profileData	
	
    def downloadProfiles(self, name, searchUrl, reqId):
	profile_list = []
	profile_links = []
	resultset = self.driver.find_element_by_xpath("//div[@class='primary-section']")

	for vcard in resultset.find_elements_by_xpath("//div[@class='professionals section']/ul/li"):
	    self.profileData = ProfileData.ProfileData()
	    self.profileData.name = name
	    self.profileData.reqId = reqId
	    
	    try:
		#Public profile link		
		self.profileData.li_profile_link = vcard.find_element_by_xpath(".//a[@class='profile-img']").get_attribute('href')	
	    except NoSuchElementException:
		print("Basic vcard not found")
	    else:
	        profile_links.append(self.profileData.li_profile_link)
	
	res=0        
	for pl in profile_links:
	    res = res+1	
	    print("Going to profile page of result " + str(res) )
	    self.driver.get(pl)


	    profile = self.scrapProfilePage(name, "false", reqId)
	    profile.downloadDate = str(date.today())	
	    profile_list.append(profile)
	    
	self.addRecordToCSV(profile_list)

    def addRecordToCSV(self, plist):
	outfile = parentdir + "/R0_profiles_raw/" + "profiles-final.csv" 	
	
        with open(outfile, 'ab') as csvfile:
    	    self.liSearchOutWriter = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8' )
	    
	    for p in plist:
		#self.printProfileData(p)
		self.liSearchOutWriter.writerow([p.reqId,
					     p.name.encode('utf-8'), 
					     p.profileFullName.encode('utf-8'),
					     p.title.encode('utf-8'),	
	         			     p.location.encode('utf-8'),
					     p.industry.encode('utf-8'),	 
				 	     p.li_profile_link.encode('utf-8'), 
				 	     p.current_work.encode('utf-8'), 
				     	     p.past_work.encode('utf-8'),
				     	     p.num_connections,	 
				     	     p.summary.encode('utf-8'), 
				     	     p.education.encode('utf-8'),
					     (",".join(p.experience)),
					     p.current_title,
					     (','.join(p.skills) ),
					     p.downloadDate.encode('utf-8'),
					     p.photoPresent,
					     p.photoFileName])

    	#csvfile.close()
    
    def printProfileData(self, profile):
	try:
            print "NAME:" + (profile.name).encode('utf-8')
	    print "TITLE:" + (profile.title).encode('utf-8')
	    print "LOCATION:" + profile.location.encode('utf-8')
	    print "INDUSTRY:" + profile.industry.encode('utf-8')
            print "CURRENT WORK:" + profile.current_work.encode('utf-8')
            print "PAST WORK:" + profile.past_work.encode('utf-8')
            print "CONNECTIONS:" + profile.num_connections
            print "SUMMARY:" + profile.summary.encode('utf-8')
            print "EDUCATION:" + profile.education.encode('utf-8')
 	    print "SKILLS:" + (','.join(profile.skills) ).encode('utf-8')
	    print "EXPERIENCE:" + ('\n\n'.join(profile.experience) )
	    print "PHOTO PRESENT:" + profile.photoPresent
	except UnicodeEncodeError:
		print("Failed while printing output")
		

if __name__ == "__main__":
    unittest.main()

