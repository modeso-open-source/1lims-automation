from typing import Any, Union

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



    def search_by_number_and_archive(self,analysis_numbers_list):
        for x in analysis_numbers_list:
            rows = self.search(x)
            if len(rows) > 0:
                self.click_check_box(source=rows[0])
                self.archive_selected_analysis()
                self.clear_search()

    def search_if_analysis_not_deleted(self,analysis_numbers_list):
        for x in analysis_numbers_list:
            rows = self.search(x)
            if len(rows) > 1:
                return True
        return False        