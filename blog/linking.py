from linkedin import linkedin


class LinkingIn():



    def __init__(self):
        self.data = []

#====== INPUTS =================
    def linked_main(self, action, searched):

        API_KEY = 'wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl'
        API_SECRET = 'daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG'
        RETURN_URL = 'mettentot.com/linker'


        authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
        authentication.authorization_url  # open this url on your browser
        application = linkedin.LinkedInApplication(authentication)

        try:
            application.get_profile()
            {u'firstName': u'ozgur',
            u'headline': u'This is my headline',
            u'lastName': u'vatansever',
            u'siteStandardProfileRequest': {u'url': u'http://www.linkedin.com/profile/view?id=46113651&authType=name&authToken=Egbj&trk=api*a101945*s101945*'}}
            val = "coming soon"
        except:
            val = "coming soon"

        return val
