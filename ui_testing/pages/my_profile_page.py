from ui_testing.pages.base_pages import BasePages
from random import randint

class MyProfile(BasePages):
    def __init__(self):
        super().__init__()
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.my_profile_url = "{}settings#myProfile".format(self.base_selenium.url)
        
    def get_my_profile_page(self):
        self.base_selenium.LOGGER.info(' + Get my profile page.')
        self.base_selenium.get(url=self.my_profile_url)
        self.sleep_small()