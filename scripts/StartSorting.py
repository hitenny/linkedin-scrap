# -*- coding: utf-8 -*-
import csv
import unicodecsv
import os
import sys
sys.path.append(os.path.abspath('modules'))
import LinkedinSorting
from Util import createdirifnotexists,fileexistordie,gettimestamp	    	
	    	
if __name__ == "__main__":
    parentdir = "Results_" + gettimestamp()
    createdirifnotexists(parentdir)

    procdir = parentdir + "/R2_profiles_HPU_proc/"
    createdirifnotexists(procdir)
    rawdir = parentdir + "/R1_profiles_HPU_raw/"

    ls = LinkedinSorting.LinkedinSorting()
    ls.sort(rawdir + "PI_raw.csv", procdir + "/PI_processed.csv")
    ls.sort(rawdir + "HI_raw.csv", procdir + "/HI_processed.csv")
    ls.sort(rawdir + "UI_raw.csv", procdir + "/UI_processed.csv")
    ls.dumpSummary()
	
	
	
