from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from uuid import uuid4
from random import randint
from ui_testing.pages.article_page import Article
from ui_testing.pages.contact_page import Contact
from ui_testing.pages.login_page import Login
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.base_pages import BasePages
from ui_testing.pages.order_page import Order
from ui_testing.pages.audit_trail_page import AuditTrail
from ui_testing.pages.contacts_page import Contacts
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from ui_testing.pages.header_page import Header
from api_testing.apis.orders_api import OrdersAPI
import datetime, re


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_selenium = BaseSelenium()

    def setUp(self):
        print('\t')
        self.base_selenium.LOGGER.info('Test case : {}'.format(self._testMethodName))
        self.base_selenium.get_driver()
        self.login_page = Login()
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.contact_page = Contact()
        self.test_unit_page = TstUnit()
        self.order_page = Order()
        self.audit_trail_page = AuditTrail()
        self.header_page = Header()
        self.base_page = BasePages()
        self.contacts_page = Contacts()
        self.article_api = ArticleAPI()
        self.test_plan_api = TestPlanAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()
        self.orders_api = OrdersAPI()

    def tearDown(self):
        self.base_selenium.quit_driver()
        self.base_selenium.LOGGER.info('TearDown. \t')

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
                elif re.search(r'\d{2}.\d{2}.\d{4}', str(item)):
                    tmp.append(datetime.datetime.strptime(item, '%d.%m.%Y'))
                elif "-" == str(item):
                    continue
                elif ' ' == str(item)[-1]:
                    tmp.append(item[:-1])
                else:
                    tmp.append(str(item).replace(',', '&').replace("'", ""))
        return tmp

    def get_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.base_selenium.LOGGER.info('Get Active article with {} test plan.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        for complete_test_plan_dict in complete_test_plans_dict:
            self.base_selenium.LOGGER.info('Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.base_selenium.LOGGER.info('Active.')
                return complete_test_plan_dict
            else:
                self.base_selenium.LOGGER.info('Archived.')
        else:
            return {}
        
    def get_multiple_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.base_selenium.LOGGER.info('Get Active articles with {} test plans.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        test_plans_list = []
        for complete_test_plan_dict in complete_test_plans_dict:
            self.base_selenium.LOGGER.info('Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.base_selenium.LOGGER.info('Active.')
                test_plans_list.append(complete_test_plan_dict)
            else:
                self.base_selenium.LOGGER.info('Archived.')
        else:
            return {}
        
        return test_plans_list

    def get_active_tst_unit_with_material_type(self, search, material_type='Raw Material'):
        self.base_selenium.LOGGER.info('Get Test Unit with  type {} .'.format(search))
        self.test_unit_page.get_test_units_page()
        test_units = self.test_unit_page.search(search)
        test_units_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit) for
                                    test_unit in test_units[:-1]]
        for test_unit_dict in test_units_dict:
            if test_unit_dict['Type'] == search and material_type in test_unit_dict['Material Type']:
                return test_unit_dict
        return {}

    def get_active_articles_with_material_type(self):
        """

        :return:
        {'material_type':[article_names]}
        """
        data = {}
        articles = self.article_api.get_all_articles().json()['articles']
        for article in articles:
            material_type = article['materialType']
            if material_type not in data.keys():
                data[material_type] = []
            data[material_type].append(article['name'])
        return data

    def info(self, message):
        self.base_selenium.LOGGER.info(message)

