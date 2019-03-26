from testconfig import config
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from UI_TESTING.elements import elements


class BaseSelenium:
    IMPLICITY_TIME = 30

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.url = config['site']['url']
        self.username = config['site']['username']
        self.password = config['site']['password']
        self.browser = config['browser']['browser'].lower()
        self.headless_mode = config['browser']['headless_mode']
        self.remote_webdriver = config['browser']['remote_driver']
        self.elements = elements

    def get_driver(self):
        if self.remote_webdriver == 'True':
            if self.browser == 'chrome':
                desired_capabilities = DesiredCapabilities.CHROME
            else:
                desired_capabilities = DesiredCapabilities.FIREFOX
            self.driver = webdriver.Remote(command_executor=self.remote_webdriver + '/wd/hub',
                                           desired_capabilities=desired_capabilities)
        else:
            if self.browser == 'chrome':
                self.driver = webdriver.Chrome()
            elif self.browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser == 'ie':
                self.driver = webdriver.Ie()
            elif self.browser == 'opera':
                self.driver = webdriver.Opera()
            elif self.browser == 'safari':
                self.driver = webdriver.Safari
        self.driver.implicitly_wait(BaseSelenium.IMPLICITY_TIME)
        self.driver.maximize_window()

    def quit_driver(self):
        self.driver.quit()

    def find_elements(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = self.driver.find_elements(getattr(By, method), value)
        else:
            self.fail("This %s method isn't defined" % method)
        return elements_value

    def find_element(self, element):
        method = self.elements[element]['method'].upper()
        value = self.elements[element]['value']
        if method in ['XPATH', 'ID', 'LINK_TEXT']:
            element_value = self.driver.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = self.driver.find_elements(getattr(By, method), value)
            if len(elements_value) > 1:
                item_order = self.elements[element]['item_order']
                if item_order == -1:
                    element_value = elements_value
                else:
                    element_value = elements_value[item_order]
            else:
                element_value = elements_value[0]
        else:
            self.fail("This %s method isn't defined" % method)
        return element_value

    def get(self, url):
        self.driver.get(url=url)

    def get_url(self):
        return self.driver.current_url

    def set_text(self, element, value):
        self.find_element(element).clear()
        self.find_element(element).send_keys(value)

    def click(self, element):
        self.find_element(element=element).click()

    def log(self, message):
        pass

    def fail(self, message):
        pass
