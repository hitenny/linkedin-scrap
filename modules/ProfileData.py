class ProfileData(object):
    def __init__(self):
	self.reqId = ""
        self.name = ""
	self.profileFullName = ""
	self.title = "NIL"
        self.location = "NIL"
	self.industry = ""
        self.li_profile_link = "NIL"
        self.current_work = ""
        self.past_work = ""
        self.num_connections = "0"	
        self.summary = "NIL"
        self.education = "NIL"
	self.experience = []
	self.current_title = ""
        self.skills = []
	self.downloadDate = ""
	self.photoPresent = "N"
	self.photoFileName = ""
	
		

class Experience(object):
    def __init__(self):
	self.title = ""
	self.company = ""
	self.speriod = ""
	self.eperiod = ""	

