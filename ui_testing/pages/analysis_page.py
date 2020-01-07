from ui_testing.pages.base_pages import BasePages
from random import randint


class Analysis(BasePages):
    def __init__(self):
        super().__init__()
        self.analysis_url = "{}analysis".format(self.base_selenium.url)

    def get_analysis_page(self):
        self.base_selenium.get(url=self.analysis_url)
        self.sleep_small()