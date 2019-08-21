from ui_testing.pages.base_pages import BasePages
from random import randint


class TstUnits(BasePages):
    def __init__(self):
        super().__init__()
        self.test_units_url = "{}testUnits".format(self.base_selenium.url)

    def get_test_units_page(self):
        self.base_selenium.LOGGER.info(' + Get test units page.')
        self.base_selenium.get(url=self.test_units_url)
        self.sleep_small()

    def get_random_test_units(self):
        row = self.base_selenium.get_table_rows(element='test_units:test_units_table')
        self.get_random_x(row=row)

    def get_random_test_units_row(self):
        return self.get_random_table_row(table_element='test_units:test_units_table')