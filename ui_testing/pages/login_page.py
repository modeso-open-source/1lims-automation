from ui_testing.pages.base_selenium import BaseSelenium


class Login:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def login(self, username, password):
        self.base_selenium.get(url=self.base_selenium.url)
        print(self.base_selenium.driver.find_element_by_xpath('//*[@id="m_login"]/div[1]/div/div/div/div[2]/div/h3').text)
        self.base_selenium.set_text(element='login:username', value=username)
        self.base_selenium.set_text(element='login:password', value=password)
        self.base_selenium.click(element='login:login_btn')
