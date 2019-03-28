from testconfig import config
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from ui_testing.elements import elements
import time


class BaseSelenium:
    IMPLICITY_TIME = 20

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
        self.wait = WebDriverWait(self.driver, BaseSelenium.IMPLICITY_TIME)

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
            item_order = self.elements[element]['item_order']
            elements_value = self.driver.find_elements(getattr(By, method), value)
            if item_order == -1:
                element_value = elements_value
            else:
                element_value = elements_value[item_order]
        else:
            self.fail("This %s method isn't defined" % method)
        return element_value

    def find_element_in_element(self, source, destination_element):
        method = self.elements[destination_element]['method'].upper()
        value = self.elements[destination_element]['value']
        if method in ['XPATH', 'ID', 'LINK_TEXT']:
            element_value = source.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            item_order = self.elements[destination_element]['item_order']
            elements_value = source.find_elements(getattr(By, method), value)
            if item_order == -1:
                element_value = elements_value
            else:
                element_value = elements_value[item_order]
        else:
            self.fail("This %s method isn't defined" % method)
        return element_value

    def check_side_list(self):
        self.wait_until_element_located('left_menu_button')
        for temp in range(5):
            try:
                if self.find_element("left_menu").location["x"] < 0:
                    self.click("left_menu_button")
                break
            except Exception as error:
                self.log(" * Can't locate the left menu. Error : %s" % error)
                time.sleep(2)

    def get(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            self.log(' * %s Exception at get(%s) ' % (str(e), url))
        else:
            self.execute_angular_script()
            self.maximize_window()

    def element_is_enabled(self, element):
        return self.find_element(element).is_enabled()

    def element_is_displayed(self, element):
        self.wait_until_element_located(element)
        return self.find_element(element).is_displayed()

    def element_background_color(self, element):
        return str(self.find_element(element).value_of_css_property('background-color'))

    def wait_until_element_located(self, element):
        method = self.elements[element]['method'].upper()
        value = self.elements[element]['value']
        for temp in range(3):
            try:
                self.wait.until(EC.visibility_of_element_located((getattr(By, method), value)))
                return True
            except:
                time.sleep(1)
        else:
            return False

    def wait_element(self, element):
        if self.wait_until_element_located(element):
            return True
        else:
            return False

    def wait_until_page_title_is(self, text, timeout=15):
        for _ in range(timeout):
            if self.driver.title == text:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def wait_until_element_located_and_has_text(self, element, text):
        method = self.elements[element][0]
        value = self.elements[element][1]
        for temp in range(10):
            try:
                self.wait.until(EC.text_to_be_present_in_element((getattr(By, method), value), text))
                return True
            except:
                time.sleep(1)
        else:
            return False

    def wait_until_element_attribute_has_text(self, element, attribute, text):
        for _ in range(10):
            try:
                if element.get_attribute(attribute) == text:
                    return True
                else:
                    time.sleep(2)
            except:
                time.sleep(3)
        else:
            return False

    def wait_unti_element_clickable(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        for temp in range(10):
            try:
                self.wait.until(EC.element_to_be_clickable((getattr(By, method), value)))
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
            else:
                return True
        else:
            self.fail('StaleElementReferenceException')

    def click(self, element):
        for temp in range(10):
            try:
                self.find_element(element).click()
                break
            except:
                time.sleep(1)
        else:
            self.fail("can't find %s element" % element)
        time.sleep(1)

    def click_item(self, element, ID):
        for temp in range(10):
            method = self.elements[element][0]
            value = self.elements[element][1]
            try:
                self.driver.find_element(getattr(By, method), value % tuple(ID)).click()
                break
            except:
                time.sleep(1)
        else:
            self.fail("can't find %s element" % element)
        time.sleep(1)

    def click_link(self, link):
        self.get(link)

    def get_text(self, element):
        for temp in range(10):
            try:
                return self.find_element(element).text
            except:
                time.sleep(0.5)
        else:
            self.fail('NoSuchElementException(%s)' % element)

    def get_size(self, element):
        self.wait_until_element_located(element)
        return self.find_element(element).size

    def get_value(self, element):
        return self.get_attribute(element, "value")

    def element_is_readonly(self, element):
        return self.get_attribute(element, "readonly")

    def element_link(self, element):
        return self.get_attribute(element, "href")

    def get_attribute(self, element, attribute):
        self.wait_until_element_located(element)
        return self.find_element(element).get_attribute(attribute)

    def get_url(self):
        try:
            curent_url = self.driver.current_url
            self.driver.ignore_synchronization = False
        except:
            self.driver.ignore_synchronization = True
            curent_url = self.driver.current_url
        return curent_url

    def set_text(self, element, value):
        self.wait_until_element_located(element)
        self.find_element(element).clear()
        self.find_element(element).send_keys(value)

    def set_text_columns(self, element, search_value, ID):
        method = self.elements[element][0]
        value = self.elements[element][1] % ID
        # self.wait_until_element_located(element)
        time.sleep(1)
        try:
            element_value = self.driver.find_element(getattr(By, method), value)
            element_value.send_keys(search_value)
            return True
        except:
            self.log("can't locate element")
            return False

    def clear_text(self, element):
        self.wait_until_element_located(element)
        self.find_element(element).clear()
        self.find_element(element).send_keys(Keys.ENTER)

    def clear_element_text(self, element):
        element.clear()
        element.send_keys(Keys.ENTER)

    def clear_text_columns(self, element, ID):
        method = self.elements[element][0]
        value = self.elements[element][1] % ID
        time.sleep(1)
        try:
            element_value = self.driver.find_element(getattr(By, method), value)
            element_value.clear()
            element_value.send_keys(Keys.ENTER)
            return True
        except:
            self.log("can't find element")
            return False

    def move_curser_to_element(self, element):
        element = self.elements[element]
        location = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, element)))
        ActionChains(self.driver).move_to_element(location).perform()

    def check_element_is_exist(self, element):
        if self.wait_element(element):
            return True
        else:
            return False

    def select(self, list_element, item_value):
        item_value = str(item_value)
        self.select_obeject = Select(self.find_element(list_element))
        self.select_list = self.select_obeject.options

        for option in self.select_list:
            if item_value in option.text:
                self.log("select %s from list" % str(option.text))
                self.select_obeject.select_by_visible_text(option.text)
                item_value = option.text
                break
        else:
            self.fail("This %s item isn't an option in %s list" % (item_value, list_element))

        self.assertEqual(item_value, self.select_obeject.first_selected_option.text)

    def get_list_items(self, list_element):
        html_list = self.find_element(list_element)
        return html_list.find_elements_by_tag_name("li")

    def get_list_items_text(self, list_element):
        compo_menu = self.get_list_items(list_element)
        compo_menu_exist = []
        for item in compo_menu:
            if item.text != "":
                if '\n' in item.text:
                    data = item.text.split('\n')
                    compo_menu_exist += data
                else:
                    compo_menu_exist.append(item.text)
        return compo_menu_exist

    def element_in_url(self, text_item):
        if " " in text_item:
            text_item = text_item.replace(" ", "%20")
        for temp in range(10):
            try:
                if text_item in self.get_url():
                    return True
            except:
                time.sleep(1)
        else:
            self.fail("this %s item isn't exist in this url: %s" % (text_item, self.get_url()))

    def get_storage_list(self):
        locations = self.environment_storage.split(',')
        if len(locations) < 2:
            return []
        else:
            return locations

    def get_table_rows(self, element=None):
        'This method return all rows in the current page else return false'
        try:
            if element == None:
                tbody = self.driver.find_element_by_tag_name('tbody')
            else:

                element = self.find_element(element)
                tbody = element.find_element_by_tag_name('tbody')

            rows = tbody.find_elements_by_tag_name('tr')
            return rows
        except:
            self.log("Can't get the tbody elements")
            return False

    def get_row_cells(self, row):
        'This method take a row and return its cells elements else return false'
        try:
            cells = row.find_elements_by_tag_name('td')
            return cells
        except:
            self.log("Can't get the row cells")
            return False

    def get_table_head_elements(self, element):
        # This method return a table head elements.
        for _ in range(10):
            try:

                table = self.find_element(element)
                thead = table.find_elements_by_tag_name('thead')
                thead_row = thead[0].find_elements_by_tag_name('tr')
                return thead_row[0].find_elements_by_tag_name('th')
            except:
                time.sleep(0.5)
        else:

            return False

    def maximize_window(self):
        time.sleep(1)
        screen_dimention = self.driver.get_window_size()
        screen_size = screen_dimention['width'] * screen_dimention['height']
        if screen_size < 1800 * 1000:
            self.driver.set_window_size(1800, 1000)

    def get_navigation_bar(self, element):
        elements = self.get_list_items(element)
        return [x.text for x in elements]

    def execute_angular_script(self):
        # This method is trying to load angular elements.
        for _ in range(30):
            if self.driver.title:
                return True
            else:
                time.sleep(2)
                try:
                    self.driver.execute_script('angular.resumeBootstrap();')
                    time.sleep(2)
                except Exception as e:
                    self.log(' * Exception : %s ' % str(e))

    def log(self, message):
        pass
    
    def fail(self, message):
        pass