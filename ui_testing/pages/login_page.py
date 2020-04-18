from ui_testing.pages.base_selenium import BaseSelenium
from selenium.common.exceptions import ElementClickInterceptedException
import time


class Login:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def login(self, username, password):
        self.base_selenium.LOGGER.info('Login {} : {}.'.format(username, password))
        self.base_selenium.get(url=self.base_selenium.url)
        self.base_selenium.set_text(element='login:username', value=username)
        self.base_selenium.set_text(element='login:password', value=password)
        try:
            self.base_selenium.click(element='login:login_btn')
        except ElementClickInterceptedException:
            self.base_selenium.click(element='login:refresh')
            self.login(username, password)

    def logout(self):
        self.base_selenium.click(element='header:header_button')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.base_selenium.click(element='header:logout_button')
        self.base_selenium.LOGGER.info('+ Logout')
        time.sleep(self.base_selenium.TIME_MEDIUM)
