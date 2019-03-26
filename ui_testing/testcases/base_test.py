from testconfig import config
from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from ui_testing.pages.login_page import Login


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_selenium = BaseSelenium()

    def setUp(self):
        self.base_selenium.get_driver()

    def tearDown(self):
        self.base_selenium.quit_driver()



