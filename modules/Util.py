import os
import sys
from datetime import date

def createdirifnotexists(dirpath):
    try:
        if not os.path.exists(dirpath):
	    os.makedirs(dirpath)
    except:
        print "Error occurred while creating dir:" + dirpath

def fileexistordie(path):
    if not os.path.exists(path):
	print "File [" + path + "] does not exist. Exiting"
	sys.exit(0)

def gettimestamp():
    return str(date.today().year) + str(date.today().month).zfill(2) + str(date.today().day).zfill(2)
