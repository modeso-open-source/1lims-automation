from ui_testing.pages.base_pages import BasePages


class Analyses(BasePages):
    def __init__(self):
        super().__init__()
        self.analysis_url = "{}analysis".format(self.base_selenium.url)

    def get_analyses_page(self):
        self.base_selenium.LOGGER.info(' + Get analyses page.')
        self.base_selenium.get(url=self.analysis_url)
        self.sleep_small()

    def search_by_number_and_archive(self, analysis_numbers_list):
        for analysis_number in analysis_numbers_list:
            rows = self.search(analysis_number)
            if len(rows) > 0:
                self.click_check_box(source=rows[0])
                self.archive_selected_items()
                self.clear_text('general:search')

    def search_if_analysis_exist(self, analysis_numbers_list):
        for analysis_number in analysis_numbers_list:
            rows = self.search(analysis_number)
            if len(rows) > 1:
                return True
        return False
