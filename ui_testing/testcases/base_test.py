from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from uuid import uuid4
import datetime


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_selenium = BaseSelenium()

    def setUp(self):
        print('\t')
        self.base_selenium.LOGGER.info('* Test case : {}'.format(self._testMethodName))
        self.base_selenium.get_driver()

    def tearDown(self):
        self.base_selenium.quit_driver()
        self.base_selenium.LOGGER.info(' * TearDown time. \t')

    def generate_random_string(self):
        return str(uuid4()).replace("-", "")[:10]

    def fix_data_format(self, data_list):
        tmp = []
        for item in data_list:
            if len(str(item)) > 0:
                if "." in str(item):
                    tmp.append(datetime.datetime.strptime(item, '%d.%m.%Y'))
                elif "-" == str(item):
                    continue
                elif ' ' == str(item)[-1]:
                    tmp.append(item[:-1])
                else:
                    str(item).replace(',', '&').replace("'", "")
                    tmp.append(item)
        return tmp
