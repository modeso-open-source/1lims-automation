from testconfig import config
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from ui_testing.elements import elements
import random, time, os, json
import pandas as pd
from loguru import logger
from contextlib import contextmanager


class PageLoadResources(object):
    """An expectation for checking that the page has been loaded

    """
    count = 0
    resources = "return window.performance.getEntriesByType('resource')"

    def __init__(self, expected_counter):
        self.expected_counter = expected_counter

    def __call__(self, driver):
        if self.count == 0:
            self.pre = len(driver.execute_script(self.resources))

        self.now = len(driver.execute_script(self.resources))

        if self.now == self.pre:
            self.count += 1
            if self.count > self.expected_counter:
                return True
        else:
            self.count = 0
        return False

class BaseSelenium:
    POLL_FREQUENCY = 0.1

    TIME_TINY = 2
    TIME_SMALL = 5
    TIME_MEDIUM = 10
    TIME_LARGE = 15
    TIME_X_LARGE = 60

    IMPLICITLY_WAIT = 60
    EXPLICITLY_WAIT = 30

    LOGGER = logger
    # LOGGER.add('log_{time}.log', backtrace=False)

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
        self.headless = config['browser']['headless'].capitalize()
        self.remote_webdriver = config['browser']['remote'].capitalize()
        self.elements = elements

    @contextmanager
    def _change_implicit_wait(self, new_value=0.001):
        self.driver.implicitly_wait(new_value)
        try:
            yield
        finally:
            self.driver.implicitly_wait(BaseSelenium.IMPLICITLY_WAIT)

    def get_driver(self):
        if self.remote_webdriver == 'True':
            if self.browser == 'chrome':
                desired_capabilities = DesiredCapabilities.CHROME
            else:
                desired_capabilities = DesiredCapabilities.FIREFOX
            self.driver = webdriver.Remote(command_executor=self.remote_webdriver + '/wd/hub',
                                           desired_capabilities=desired_capabilities)
        elif self.headless == 'True':
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_experimental_option("prefs", {
                "download.default_directory": os.path.expanduser("~/Downloads"),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
            })
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            if self.browser == 'chrome':
                options = Options()
                options.add_argument('--ignore-certificate-errors')
                self.driver = webdriver.Chrome(chrome_options=options)
            elif self.browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser == 'ie':
                self.driver = webdriver.Ie()
            elif self.browser == 'opera':
                self.driver = webdriver.Opera()
            elif self.browser == 'safari':
                self.driver = webdriver.Safari
        self.driver.implicitly_wait(BaseSelenium.IMPLICITLY_WAIT)
        # self.driver.set_window_position(0, 0)

        self.driver.set_window_size(1800, 1200)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, BaseSelenium.EXPLICITLY_WAIT, BaseSelenium.POLL_FREQUENCY)

    def quit_driver(self):
        self.driver.quit()

    def get_method_value_order(self, element):
        element_page, element_name = element.split(':')
        method = self.elements[element_page][element_name]['method'].upper()
        value = self.elements[element_page][element_name]['value']
        if 'order' in self.elements[element_page][element_name]:
            order = self.elements[element_page][element_name]['order']
        else:
            order = None
        return method, value, order

    def find_elements(self, element):
        method, value, order = self.get_method_value_order(element=element)
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CLASS_NAME', 'NAME', 'TAG_NAME', 'CSS_SELECTOR']:
            elements_value = self.driver.find_elements(getattr(By, method), value)
            return elements_value
        else:
            self.LOGGER.error(" This %s method isn't defined" % method)
            raise BaseException

    def find_element(self, element):
        method, value, order = self.get_method_value_order(element=element)
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CSS_SELECTOR']:
            element_value = self.driver.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = self.driver.find_elements(getattr(By, method), value)
            if order == -1:
                element_value = elements_value
            else:
                element_value = elements_value[order]
        else:
            self.LOGGER.error(" This %s method isn't defined" % method)
            raise BaseException
        return element_value

    def find_element_in_element(self, destination_element, source_element='', source=''):
        if not source:
            source = self.find_element(element=source_element)
        method, value, order = self.get_method_value_order(element=destination_element)
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CSS_SELECTOR']:
            element_value = source.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = source.find_elements(getattr(By, method), value)
            if order == -1:
                element_value = elements_value
            else:
                element_value = elements_value[order]
        else:
            self.LOGGER.error(" This %s method isn't defined" % method)
            raise BaseException
        return element_value

    def find_elements_in_element(self, destination_element, source_element='', source=''):
        if not source:
            source = self.find_element(element=source_element)
        method, value, order = self.get_method_value_order(element=destination_element)
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CSS_SELECTOR']:
            element_value = source.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = source.find_elements(getattr(By, method), value)
            return elements_value
        else:
            self.LOGGER.error(" This %s method isn't defined" % method)
            raise BaseException
        return element_value

    def get(self, url, sleep=0):
        self.driver.get(url)
        time.sleep(sleep)

    def element_background_color(self, element):
        return str(self.find_element(element).value_of_css_property('background-color'))

    def element_is_displayed(self, element):
        return self.find_element(element).is_displayed()

    def element_is_enabled(self, element):
        return self.find_element(element).is_enabled()

    def wait_until_element_located(self, element):
        method, value, order = self.get_method_value_order(element=element)
        if order == 0:
            with self._change_implicit_wait():
                return self.wait.until(EC.visibility_of_element_located((getattr(By, method), value)))
        else:
            with self._change_implicit_wait():
                dom_element = self.find_element(element=element)
                end_time = time.time() + BaseSelenium.EXPLICITLY_WAIT
                while True:
                    if dom_element.is_displayed():
                        return dom_element
                    else:
                        time.sleep(0.5)
                    if time.time() > end_time:
                        break
                raise TimeoutException()

    def wait_until_element_is_not_displayed(self, element):
        method, value, order = self.get_method_value_order(element=element)
        if order in [0, None]:
            with self._change_implicit_wait():
                return self.wait.until(EC.invisibility_of_element_located((getattr(By, method), value)))
        else:
            with self._change_implicit_wait():
                dom_element = self.find_element(element=element)
                end_time = time.time() + BaseSelenium.EXPLICITLY_WAIT
                while True:
                    if dom_element.is_displayed():
                        time.sleep(0.5)
                    else:
                        return dom_element
                    if time.time() > end_time:
                        break
                raise TimeoutException("Element is still displayed")

    def wait_until_element_clickable(self, element):
        method, value, order = self.get_method_value_order(element=element)
        if order == 0:
            with self._change_implicit_wait():
                return self.wait.until(EC.element_to_be_clickable((getattr(By, method), value)))
        else:
            with self._change_implicit_wait():
                end_time = time.time() + BaseSelenium.EXPLICITLY_WAIT
                while True:
                    try:
                        dom_element = self.find_element(element=element)
                    except:
                        time.sleep(0.5)
                        if time.time() > end_time:
                            break
                        continue

                    if dom_element.is_displayed() and dom_element.is_enabled():
                        return dom_element
                    else:
                        time.sleep(0.5)
                        if time.time() > end_time:
                            break
                raise TimeoutException("Element is not disabled or enabled")

    def wait_until_element_located_and_has_text(self, element, text):
        method, value, order = self.get_method_value_order(element=element)
        if order == 0:
            with self._change_implicit_wait():
                return self.wait.until(EC.text_to_be_present_in_element((getattr(By, method), value), text))
        else:
            with self._change_implicit_wait():
                dom_element = self.find_element(element=element)
                end_time = time.time() + BaseSelenium.EXPLICITLY_WAIT
                while True:
                    if text in dom_element.text:
                        return dom_element
                    else:
                        time.sleep(0.5)
                    if time.time() > end_time:
                        break
                raise TimeoutException()

    def wait_element(self, element):
        try:
            self.wait_until_element_located(element)
            return True
        except:
            return False

    def wait_until_page_title_is(self, text, timeout=15):
        for _ in range(timeout):
            if self.driver.title == text:
                return True
            else:
                time.sleep(1)
        else:
            raise TimeoutException()

    def wait_until_page_url_has(self, text, timeout=15):
        for _ in range(timeout):
            if text in self.driver.current_url:
                return True
            else:
                time.sleep(0.5)
        else:
            raise TimeoutException()

    def wait_until_page_load_resources(self, expected_counter=10):
        self.wait.until(PageLoadResources(expected_counter))

    def click(self, element):
        dom_element = self.wait_until_element_clickable(element=element)
        dom_element.click()

    def click_by_script(self, element):
        dom_element = self.wait_until_element_clickable(element=element)
        self.driver.execute_script('arguments[0].click();', dom_element)

    def click_item(self, element, ID):
        for temp in range(10):
            method, value, order = self.get_method_value_order(element=element)
            try:
                self.driver.find_element(getattr(By, method), value % tuple(ID)).click()
                break
            except:
                time.sleep(1)
        else:
            self.LOGGER.warning(" can't find %s element" % element)
        time.sleep(1)

    def click_link(self, link):
        self.get(link)

    def get_text(self, element):
        self.wait_until_element_located(element)
        return self.find_element(element).text

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

    def clear_text(self, element):
        self.wait_until_element_located(element)
        self.find_element(element).clear()
        self.find_element(element).send_keys(Keys.ENTER)

    def clear_element_text(self, element):
        element = self.find_element(element)
        element.clear()
        element.send_keys(Keys.ENTER)

    def clear_items_in_drop_down(self, element, confirm_popup=False, one_item_only=False):
        # element is ng-select element
        # make sure that there are elements to be deleted
        self.wait_until_element_located(element)
        ng_values = self.find_element_in_element(destination_element='general:ng_values', source_element=element)
        ng_values.reverse()
        for ng_value in ng_values:
            cancel = self.find_element_in_element(destination_element='general:cancel_span', source=ng_value)
            cancel.click()
            if confirm_popup:
                if self.check_element_is_exist(element='general:form_popup_warning_window'):
                    self.click(element='order:confirm_pop')
            if one_item_only:
                break

    def clear_single_select_drop_down(self, element):
        self.wait_until_element_located(element)
        clear_button = self.find_element_in_element(destination_element='general:clear_single_dropdown',
                                                    source_element=element)
        clear_button.click()

    def clear_items_with_text_in_drop_down(self, element, items_text=[]):
        # element is ng-select element
        # make sure that there are elements to b deleted
        self.wait_until_element_located(element)
        ng_values = self.find_element_in_element(destination_element='general:ng_values', source_element=element)
        for ng_value in ng_values:
            if ng_value.text in items_text:
                cancel = self.find_element_in_element(destination_element='general:cancel_span', source=ng_value)
                cancel.click()

    def is_text_included_in_drop_down_items(self, element, item_text):
        self.wait_until_element_located(element)
        ng_values = self.find_element_in_element(destination_element='general:ng_values', source_element=element)
        for ng_value in ng_values:
            if item_text in ng_value.text:
                return self.find_element_in_element(destination_element='general:cancel_span', source=ng_value)

    def check_element_is_exist(self, element):
        if self.wait_element(element):
            return True
        else:
            return False

    def check_element_is_not_exist(self, element):
        try:
            self.wait_until_element_is_not_displayed(element)
            return True
        except TimeoutException:
            return False
        except:
            return True

    def select_random_item(self, element):
        items = self.find_elements(element=element)
        if len(items) <= 1:
            return
        items[random.randint(0, len(items) - 1)].click()

    def select_item_from_items(self, item_text, items_element):
        items = self.find_elements(element=items_element)
        for item in items:
            if item_text == item.text:
                item.click()
                break

    def select_item_from_drop_down(self, element='', element_source='', item_text='', avoid_duplicate=False,
                                   options_element='general:drop_down_options'):
        """

        :param element: element refer to ng-select dom item.
        :param element_source:  dom item.
        :param item_text:
        :param avoid_duplicate:
        :param options_element:
        :return:
        """
        if element:
            if 'ng-select-disabled' in self.get_attribute(element=element, attribute='class'):
                self.LOGGER.info(' Drop-down is disabled')
                return False

        if item_text:
            if element:
                input_element = self.find_element_in_element(destination_element='general:input',
                                                             source_element=element)
            else:  # if element_source
                input_element = self.find_element_in_element(destination_element='general:input',
                                                             source=element_source)
            time.sleep(self.TIME_TINY)
            input_element.send_keys(item_text)
        else:
            if element_source:
                element_source.click()
            else:
                self.click(element=element)
        time.sleep(self.TIME_SMALL)

        items = self.find_elements(element=options_element)
        if not item_text:  # random selection
            if len(items) == 1 and items[0].text:  # if only one item in list
                items[0].click()
                return True
            elif len(items) <= 1:
                self.LOGGER.info(' There is no drop-down options')
                return False

            if avoid_duplicate:
                items[random.choice(self._unique_index_list(data=items))].click()
                return True
            else:
                items[random.randint(0, len(items) - 1)].click()
                return True
        else:
            if item_text not in [item.text for item in items]:
                time.sleep(self.TIME_TINY)
                items = self.find_elements(element=options_element)
            for item in items:
                if item_text in item.text:
                    item.click()
                    return True
            else:
                self.LOGGER.info(' There is no {} option in the drop-down'.format(item_text))
                return False

    def is_item_in_drop_down(self, element, item_text, options_element='general:drop_down_options'):
        """

        :param element: element refer to ng-select dom item.
        :param element_source:  dom item.
        :param item_text:
        :param avoid_duplicate:
        :param options_element:
        :return:
        """
        for item in self.get_drop_down_suggestion_list(element, item_text, options_element):
            if item_text in item:
                return True
        else:
            return False

    def _unique_index_list(self, data):  # I didnt like this implemenation need to fix it!+
        result = []
        data_text = [data_item.text for data_item in data]
        for text in data_text:
            _occurrences = [index for index, value in enumerate(data_text) if
                            value == text]  # this returns the indexs for each item
            if len(_occurrences) == 1:
                result.append(_occurrences[0])
        return result

    def _is_item_a_drop_down(self, item):
        """
        item: dom element
        :return: True if the item is a drop down, False if it is not.
        """
        if item.find_element_by_tag_name('input').get_attribute('role') == 'combobox':
            return True
        else:
            return False

    def get_drop_down_suggestion_list(self, element, item_text, options_element='general:drop_down_options'):
        """

        :param element: element refer to ng-select dom item.
        :param item_text:
        :param avoid_duplicate:
        :param options_element:
        :return:
        """
        if 'ng-select-disabled' in self.get_attribute(element=element, attribute='class'):
            self.LOGGER.info('Drop-down is disabled')
            return False

        input_element = self.find_element_in_element(destination_element='general:input', source_element=element)
        input_element.send_keys(item_text)
        time.sleep(self.TIME_SMALL)

        items = self.find_elements(element=options_element)
        return [item.text for item in items]

    def update_item_value(self, item, item_text=''):
        """
        If the item is drop down, it Will try to select item text to be it's value.
        If not and it has an input field, then it will update this input field.
        :param item:
        :param item_text:
        :return:
        """
        if self._is_item_a_drop_down(item):
            self.select_item_from_drop_down(element_source=item, item_text=item_text)
        else:
            input_item = self.find_element_in_element(source=item, destination_element='general:input')
            input_item.clear()
            input_item.send_keys(item_text)

    def set_text_in_drop_down(self, ng_select_element, text, input_element='general:input',
                              confirm_button='general:drop_down_options'):
        input_field = self.find_element_in_element(destination_element=input_element, source_element=ng_select_element)
        input_field.send_keys(text)
        confirm_button = self.find_elements(confirm_button)
        confirm_button[0].click()

    def check_item_in_items(self, element, item_text, options_element='general:drop_down_options'):
        self.click(element=element)
        items = self.find_elements(element=options_element)
        for item in items:
            if item_text == item.text:
                return True
        else:
            return False

    def check_item_partially_in_items(self, element, item_text, options_element='general:drop_down_options'):
        self.click(element=element)
        items = self.find_elements(element=options_element)
        for item in items:
            if item_text in item.text:
                return True
        else:
            return False

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
            self.LOGGER.warning(" this %s item isn't exist in this url: %s" % (text_item, self.get_url()))

    def get_table_rows(self, element=None, source=None):
        'This method return all rows in the current page else return false'
        if source:
            tbody = source.find_element_by_tag_name('tbody')
            rows = tbody.find_elements_by_tag_name('tr')
            return rows
        else:
            try:
                if element == None:
                    tbody = self.driver.find_element_by_tag_name('tbody')
                else:
                    element = self.find_element(element)
                    tbody = element.find_element_by_tag_name('tbody')

                rows = tbody.find_elements_by_tag_name('tr')
                return rows
            except:
                self.LOGGER.exception(" Can't get the tbody elements")
                return []

    def get_row_cells(self, row):
        'This method take a row and return its cells elements else return false'
        try:
            cells = row.find_elements_by_tag_name('td')
            return cells
        except:
            self.LOGGER.exception(" Can't get the row cells")
            return []

    def get_table_head_elements(self, element):
        try:
            table = self.find_element(element)
            thead = table.find_elements_by_tag_name('thead')
            # thead_row = thead[0].find_elements_by_tag_name('tr')
            # return thead_row[0].find_elements_by_tag_name('th')
            return thead[0].find_elements_by_tag_name('th')
        except:
            self.LOGGER.exception(" Can't get table head.")
            return []

    def get_table_head_elements_with_tr(self, element):
        try:
            table = self.find_element(element)
            thead = table.find_elements_by_tag_name('thead')
            thead_row = thead[0].find_elements_by_tag_name('tr')
            # return thead_row[0].find_elements_by_tag_name('th')
            return thead_row
        except:
            self.LOGGER.exception(" Can't get table head.")
            return []

    def get_row_cell_text_related_to_header(self, row, column_value):
        """

        :param row: table row selenium item
        :param column_value: table column value
        :return:
        """
        row_dict = self.get_row_cells_dict_related_to_header(row=row)
        return row_dict[column_value]

    def get_row_cells_dict_related_to_header(self, row, table_element='general:table'):
        cells_dict = {}
        headers = self.get_table_head_elements(element=table_element)
        headers_text = [header.text for header in headers]
        row_cells = self.get_row_cells(row=row)
        row_text = [cell.text for cell in row_cells]
        if len(row_text) > 1:
            for column_value in headers_text:
                cells_dict[column_value] = row_text[headers_text.index(column_value)]

        return cells_dict

    def get_rows_cells_dict_related_to_header(self, table_element='general:table'):
        result = []
        headers = self.get_table_head_elements(element=table_element)
        headers_text = [header.text for header in headers]
        for row in self.get_table_rows(element=table_element):
            row_cells = self.get_row_cells(row=row)
            row_text = [cell.text for cell in row_cells]
            if row_text != ['']:
                cells_dict = {}
                for column_value in headers_text:
                    cells_dict[column_value] = row_text[headers_text.index(column_value)]
                result.append(cells_dict)
        return result

    def get_row_cells_id_dict_related_to_header(self, row, table_element='general:table'):
        cells_dict = {}
        headers = self.get_table_head_elements(element=table_element)
        headers_id = [header.find_element_by_tag_name('label').get_attribute('id') for header in headers]
        row_cells = self.get_row_cells(row=row)
        row_text = [cell.text for cell in row_cells]

        for column_id in headers_id:
            cells_dict[column_id] = row_text[headers_id.index(column_id)]

        return cells_dict

    def get_row_cells_elements_related_to_header(self, row, table_element='general:table'):
        cells_elements = {}
        headers = self.get_table_head_elements(element=table_element)
        headers_text = [header.text for header in headers]
        row_cells = self.get_row_cells(row=row)

        for column_value in headers_text:
            cells_elements[column_value] = row_cells[headers_text.index(column_value)]

        return cells_elements

    def get_row_cells_id_elements_related_to_header(self, row, table_element='general:table'):
        cells_elements = {}
        headers = self.get_table_head_elements(element=table_element)
        headers_id = [header.find_element_by_tag_name('label').get_attribute('id') for header in headers]
        row_cells = self.get_row_cells(row=row)

        for column_id in headers_id:
            cells_elements[column_id] = row_cells[headers_id.index(column_id)]

        return cells_elements

    def select_multiple_table_rows_by_header_values(self, header, list_of_value, table_element='general:table'):
        for row in self.get_table_rows(element=table_element):
            row_data = self.get_row_cells_dict_related_to_header(row=row)
            if row_data:
                if row_data[header] in list_of_value:
                    check_box = self.find_element_in_element(
                        destination_element='general:checkbox', source=row)
                    check_box.click()

    def maximize_window(self):
        time.sleep(1)
        screen_dimention = self.driver.get_window_size()
        screen_size = screen_dimention['width'] * screen_dimention['height']
        if screen_size < 1800 * 1000:
            self.driver.set_window_size(1800, 1000)

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
                    self.LOGGER.exception(' * Exception : %s ' % str(e))

    def download_excel_file(self, element, sleep=30):
        self.click(element=element)
        time.sleep(sleep)
        sheets = []

        home_download = os.path.expanduser("~/Downloads/")
        downloaded_file_path = home_download if os.path.isdir(home_download) else "./"
        for file_name in os.listdir(os.path.expanduser(downloaded_file_path)):
            if '.xlsx' in file_name:
                sheets.append(os.path.expanduser(downloaded_file_path) + file_name)

        downloaded_file_name = max(sheets, key=os.path.getctime)
        data = pd.read_excel(downloaded_file_name)
        # row = data.iloc[1]
        # values = row.values
        return data

    def scroll(self, up=True):
        if up:
            self.driver.execute_script('window.scrollTo(0, -1*document.body.scrollHeight);')
        else:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def paste(self, element):
        self.LOGGER.info('paste value from clipboard.')
        self.wait_until_element_located(element)
        dom_element = self.find_element(element)
        dom_element.clear()
        dom_element.send_keys(Keys.CONTROL, 'v')

    def refresh(self):
        self.driver.refresh()
        time.sleep(5)

    def find_element_by_xpath(self, xpath=''):
        return self.driver.find_element_by_xpath(xpath)

    def set_local_storage(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key,
                                   json.dumps(value))
