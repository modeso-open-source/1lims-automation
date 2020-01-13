from ui_testing.pages.base_pages import BasePages

class AllAnalysesPage(BasePages):
    def __init__(self):
        super().__init__()
        self.analyses = "{}sample/analysis".format(self.base_selenium.url)


    def get_analysis_page(self):
        self.base_selenium.get(url=self.analyses)
        self.sleep_medium()

