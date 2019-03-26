from UI_TESTING.pages.base_selenium import BaseSelenium


class Login:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def login(self, username, password):
        self.base_selenium.get(url=self.base_selenium.url)
        self.base_selenium.set_text(element='username', value=username)
        self.base_selenium.set_text(element='password', value=password)
        self.base_selenium.click(element='login_btn')

