from Util import fileexistordie,gettimestamp

KW_PROFESSION_GENERAL = []
KW_PROFESSION_TITLE = []
KW_PROFESSION_SPEC = []
KW_WORKING_STATUS = []
KW_INDUSTRY_M = []
KW_GEOGRAPHY_M = []
KW_NON_PROFESSION = []
KW_WORK_LOCATION = []

configdir = "Config_" + gettimestamp()
fileexistordie(configdir)

prof_gen_file = configdir + "/C1_KW/" + "KW_Profession_general.txt"
prof_title_file = configdir + "/C1_KW/" + "KW_Profession_title.txt"
prof_spec_file = configdir + "/C1_KW/" + "KW_Profession_spec.txt"
prof_ws_file = configdir + "/C1_KW/" + "KW_Working_status.txt"
prof_ind_file = configdir + "/C1_KW/" + "KW_Industry_M.txt"
prof_geo_file = configdir + "/C1_KW/" + "KW_Geography_M.txt"
prof_nonprof_file = configdir + "/C1_KW/" + "KW_non-profession_titles.txt"
prof_loc_file = configdir + "/C1_KW/" + "KW_Working_place.txt"

fileexistordie(prof_gen_file)
fileexistordie(prof_title_file)
fileexistordie(prof_spec_file)
fileexistordie(prof_ws_file)
fileexistordie(prof_ind_file)
fileexistordie(prof_geo_file)
fileexistordie(prof_nonprof_file)
fileexistordie(prof_loc_file)

def loadKeywords(fh, kwlname):
    for line in fh:
	kwlname.append(line.rstrip())
	
def readKeywordFile():
    global KW_PROFESSION_GENERAL
    global KW_PROFESSION_TITLE
    global KW_PROFESSION_SPEC
    global KW_WORKING_STATUS
    global KW_INDUSTRY_M
    global KW_GEOGRAPHY_M
    global KW_NON_PROFESSION
    global KW_WORK_LOCATION

    print "Loading General\n"	
    f = open(prof_gen_file, 'r')
    loadKeywords(f,KW_PROFESSION_GENERAL)
    print str(len(KW_PROFESSION_GENERAL)) + " words loaded\n"	

    print "Loading Titles\n"	
    f = open(prof_title_file, 'r')
    loadKeywords(f,KW_PROFESSION_TITLE)
    print str(len(KW_PROFESSION_TITLE)) + " words loaded\n"

    print "Loading Spec\n"
    f = open(prof_spec_file, 'r')
    loadKeywords(f,KW_PROFESSION_SPEC)
    print str(len(KW_PROFESSION_SPEC)) + " words loaded\n"

    print "Loading Work status\n"
    f = open(prof_ws_file, 'r')
    loadKeywords(f,KW_WORKING_STATUS)
    print str(len(KW_WORKING_STATUS)) + " words loaded\n"
 
    print "Loading Industry\n"
    f = open(prof_ind_file, 'r')
    loadKeywords(f,KW_INDUSTRY_M)
    print str(len(KW_INDUSTRY_M)) + " words loaded\n"

    print "Loading Geography\n"
    f = open(prof_geo_file, 'r')
    loadKeywords(f,KW_GEOGRAPHY_M)
    print str(len(KW_GEOGRAPHY_M)) + " words loaded\n"

    print "Loading non profession title\n"
    f = open(prof_nonprof_file, 'r')
    loadKeywords(f,KW_NON_PROFESSION)
    print str(len(KW_NON_PROFESSION)) + " words loaded\n"

    print "Loading Work location\n"
    f = open(prof_loc_file, 'r')
    loadKeywords(f,KW_WORK_LOCATION)
    print str(len(KW_WORK_LOCATION)) + " words loaded\n"

def getConfigValue(key):
    return conf[key]
    
      
