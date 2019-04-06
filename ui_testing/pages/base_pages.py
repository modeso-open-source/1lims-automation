from uuid import uuid4
from ui_testing.pages.base_selenium import BaseSelenium
import time

class BasePages:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def generate_random_text(self):
        return str(uuid4()).replace("-", "")[:10]

    def search(self, value):
        """
        Search for a specific value
        :param value:
        :return: The first element in the search table
        """
        self.base_selenium.set_text(element='general:search', value=value)
        self.base_selenium.click(element='general:search')
        time.sleep(self.base_selenium.TIME_SMALL)
        rows = self.base_selenium.get_table_rows(element='general:table')
        if len(rows) > 0:
            return rows[0]
        else:
            return None

    def sleep_tiny(self):
        time.sleep(self.base_selenium.TIME_TINY)

    def sleep_small(self):
        time.sleep(self.base_selenium.TIME_SMALL)

    def sleep_medium(self):
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def sleep_large(self):
        time.sleep(self.base_selenium.TIME_LARGE)

    def save(self):
        self.base_selenium.click(element='general:save')
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def cancel(self, force=True):
        self.base_selenium.click(element='general:cancel')
        if self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'):
            if force:
                self.base_selenium.click(element='general:confirm_pop')
            else:
                self.base_selenium.click(element='general:confirm_cancel')
        time.sleep(self.base_selenium.TIME_MEDIUM)
