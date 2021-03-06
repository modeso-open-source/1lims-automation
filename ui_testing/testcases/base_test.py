from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from uuid import uuid4
from random import randint
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from api_testing.apis.base_api import BaseAPI
import datetime, re, os, shutil


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        cls.create_screenshots_dir()
        cls.base_selenium = BaseSelenium()
        cls.base_selenium.get_driver()
        cls.base_selenium.get(url=cls.base_selenium.url)
        cls.pass_refresh_feature()
        cls.set_authorization(auth=BaseAPI().AUTHORIZATION_RESPONSE)

    def setUp(self):
        print('\t')
        self.info('Test case : {}'.format(self._testMethodName))
        # self.base_selenium.get(url=self.base_selenium.url)
        # self.base_selenium.wait_until_page_load_resources()

    def tearDown(self):
        self.screen_shot()
        self.info('go to dashboard page')
        self.base_selenium.get(url=f"{self.base_selenium.url}dashboard")
        self.info('TearDown. \t')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.base_selenium.quit_driver()

    def screen_shot(self):
        try:
            method, error = self._outcome.errors[0]
            if error:
                screen_shot = f"./screenshots/screenshot_{method._testMethodName}_.png"
                self.info(f"saved error screen shot : {screen_shot}")
                self.base_selenium.driver.get_screenshot_as_file(
                    f"./screenshots/screenshot_{method._testMethodName}_.png")
        except:
            pass

    def generate_random_string(self):
        return str(uuid4()).replace("-", "")[:10]

    def generate_random_number(self, lower=1, upper=100000):
        return randint(lower, upper)

    def fix_data_format(self, data_list):
        tmp = []
        for item in data_list:
            if len(str(item)) > 0:
                if re.search(r'\d{2}.\d{2}.\d{4},\s\d{1,2}:\d{1,2}\s(A|P)M', str(item)):
                    tmp.append(datetime.datetime.strptime(item, '%d.%m.%Y, %H:%M %p'))
                elif re.search(r'\d{2}\.\d{2}\.\d{4}', str(item)):
                    tmp.append(datetime.datetime.strptime(item, '%d.%m.%Y'))
                elif str(item) in ["-", "nan", "N/A"]:
                    continue
                elif ',' in str(item) and '&' in str(item):
                    item = str(item).replace('&', ',')
                    tmp.extend(str(item).split(','))
                elif ',' in str(item):
                    tmp.extend(str(item).split(','))
                elif ', ' in str(item):
                    tmp.extend(str(item).split(', '))
                elif '&' in str(item):
                    tmp.extend(str(item).split('&'))
                elif ' ' == str(item)[-1]:
                    tmp.append(item[:-1])
                elif 'all' == str(item)[-1]:
                    tmp.append('All')
                else:
                    tmp.append(str(item).replace(',', '&').replace("'", "").replace(' - ', '-'))

        return tmp

    def reformat_data(self, data_list):
        tmp = []
        for item in data_list:
            if len(str(item)) > 0:
                tmp.append(str(item).replace(',', ' &').replace("'", ""))
        return tmp

    def get_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.info('Get Active article with {} test plan.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        for complete_test_plan_dict in complete_test_plans_dict:
            self.info(
                'Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.info('Active.')
                return complete_test_plan_dict
            else:
                self.info('Archived.')
        else:
            return {}

    def get_multiple_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.info('Get Active articles with {} test plans.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        test_plans_list = []
        for complete_test_plan_dict in complete_test_plans_dict:
            self.info(
                'Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.info('Active.')
                test_plans_list.append(complete_test_plan_dict)
            else:
                self.LOGGER.info('Archived.')
        else:
            return {}

        return test_plans_list

    def get_active_tst_unit_with_material_type(self, search, material_type='Raw Material'):
        self.test_unit_page = TstUnit()
        self.info('Get Test Unit with  type {} .'.format(search))
        self.test_unit_page.get_test_units_page()
        test_units = self.test_unit_page.search(search)
        test_units_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit) for
                           test_unit in test_units[:-1]]
        for test_unit_dict in test_units_dict:
            if test_unit_dict['Type'] == search and material_type in test_unit_dict['Material Type']:
                return test_unit_dict
        return {}

    '''
    Removes the data that was changed in the duplication process in order to compare
    between the objects to make sure that the duplication was done correcly.
    '''

    def remove_unduplicated_data(self, data_changed=[], first_element=[], second_element=[]):
        for data in data_changed:
            if data in first_element and data in second_element:
                if first_element[data] != None:
                    del first_element[data]
                if second_element[data] != None:
                    del second_element[data]

        return first_element, second_element

    @property
    def info(self):
        return self.base_selenium.LOGGER.info

    @property
    def debug(self):
        return self.base_selenium.LOGGER.debug

    @classmethod
    def set_authorization(cls, auth):
        if "Admin" == auth.get('role'):
            del auth['role']
            auth['roles'] = ["Admin"]
        cls.base_selenium.set_local_storage('modeso-auth-token', auth)

    @classmethod
    def pass_refresh_feature(cls):
        with cls.base_selenium._change_implicit_wait(new_value=2):
            try:
                cls.base_selenium.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
            except:
                pass

    @staticmethod
    def create_screenshots_dir():
        dir = 'screenshots'
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=True)
        os.mkdir(dir)
