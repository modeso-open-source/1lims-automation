from ui_testing.pages.base_pages import BasePages

class CompanyProfile(BasePages):
    def __init__(self):
        super().__init__()
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_url = "{}settings#companyProfile".format(self.base_selenium.url)

    def get_company_profile_page(self):
        self.base_selenium.get(url=self.company_profile_url)
        self.sleep_small()