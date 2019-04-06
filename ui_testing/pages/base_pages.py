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
