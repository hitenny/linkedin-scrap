class Kwstats(object):
    def __init__(self):
        self.KW_hits = {
	"KW_PROFESSION_GENERAL" : 0,
	"KW_PROFESSION_TITLE" : 0,
	"KW_PROFESSION_SPEC" : 0,
	"KW_WORKING_STATUS" : 0,
	"KW_INDUSTRY_M" : 0,
	"KW_GEOGRAPHY_M" : 0,
	"KW_NON_PROFESSION" : 0,
	"KW_WORK_LOCATION" : 0
	}

	self.KW_high_interest_hits = 0 	#Hit in General, Spec, Title
	self.KW_possible_interest_hits = 0 	#Hit in Industry NO Hit in General, Title, Spec, Non-profession
	self.KW_uninterest_1_hits = 0	#No hit in General, Spec, Title, Industry
	self.KW_uninterest_2_hits = 0	#No hit in General, Spec, Title, Industry AND Hit in Industry, Non-Profession
