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

    def archive_selected_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:archive')
        self.confirm_popup()

    def get_archived_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:archived')
        self.sleep_small()

    def is_test_unit_in_table(self, value):
        """
            - get_archived_test_units then call me to check if the test unit has been archived.
            - get_active_test_units then call me to check if the test unit is active.
        :param value: search value
        :return:
        """
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def restore_selected_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:restore')
        self.confirm_popup()

    def get_active_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:active')
        self.sleep_small()