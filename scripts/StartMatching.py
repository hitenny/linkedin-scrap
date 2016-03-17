# -*- coding: utf-8 -*-
import csv
import unicodecsv
import os
import sys
sys.path.append(os.path.abspath('modules'))
import KeywordFileReader	    	
import LinkedinMatch
	    	
if __name__ == "__main__":
	KeywordFileReader.readKeywordFile()
	lm = LinkedinMatch.LinkedinMatch()
	lm.match()
