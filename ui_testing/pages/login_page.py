from ui_testing.pages.base_selenium import BaseSelenium
from selenium.common.exceptions import ElementClickInterceptedException


class Login:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def login(self, username, password):
        self.base_selenium.get(url=self.base_selenium.url)
        self.base_selenium.set_text(element='login:username', value=username)
        self.base_selenium.set_text(element='login:password', value=password)
        try:
            self.base_selenium.click(element='login:login_btn')
        except ElementClickInterceptedException:
            self.base_selenium.click(element='login:refresh')
            self.login(username, password)
