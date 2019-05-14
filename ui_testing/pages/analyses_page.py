from ui_testing.pages.base_pages import BasePages

class Analyses(BasePages):
    def __init__(self):
        super().__init__()
        self.analysis_url = "{}analysis".format(self.base_selenium.url)

    def get_analyses_page(self):
        self.base_selenium.get(url=self.analysis_url)

    def archive_selected_analysis(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archive')
        self.confirm_popup()