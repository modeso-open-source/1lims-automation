from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from uuid import uuid4
from ui_testing.pages.analyses_page import Analyses
from ui_testing.pages.article_page import Article
from ui_testing.pages.login_page import Login
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_plan_api import TestPlanAPI
import datetime


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_selenium = BaseSelenium()

    def setUp(self):
        print('\t')
        self.base_selenium.LOGGER.info('* Test case : {}'.format(self._testMethodName))
        self.base_selenium.get_driver()
        self.login_page = Login()
        self.order_page = Order()
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.analyses_page = Analyses()
        self.orders_page = Orders()
        self.test_unit_page = TstUnit()

        self.article_api = ArticleAPI()
        self.test_plan_api = TestPlanAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()

    def tearDown(self):
        self.base_selenium.quit_driver()
        self.base_selenium.LOGGER.info(' * TearDown. \t')

    def generate_random_string(self):
        return str(uuid4()).replace("-", "")[:10]

    def fix_data_format(self, data_list):
        tmp = []
        for item in data_list:
            if len(str(item)) > 0:
                if "." in str(item):
                    tmp.append(datetime.datetime.strptime(item, '%d.%m.%Y'))
                elif "-" == str(item):
                    continue
                elif ' ' == str(item)[-1]:
                    tmp.append(item[:-1])
                else:
                    tmp.append(str(item).replace(',', '&').replace("'", ""))
        return tmp

    def get_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.base_selenium.LOGGER.info(' + Get Active article with {} test plan.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        for complete_test_plan_dict in complete_test_plans_dict:
            self.base_selenium.LOGGER.info(' + Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.base_selenium.LOGGER.info(' + Active.')
                return complete_test_plan_dict
            else:
                self.base_selenium.LOGGER.info(' + Archived.')
        else:
            return {}
        
    def get_multiple_active_article_with_tst_plan(self, test_plan_status='complete'):
        self.base_selenium.LOGGER.info(' + Get Active articles with {} test plans.'.format(test_plan_status))
        self.test_plan.get_test_plans_page()
        complete_test_plans = self.test_plan.search(test_plan_status)
        complete_test_plans_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=complete_test_plan) for
                                    complete_test_plan in complete_test_plans[:-1]]

        self.article_page.get_articles_page()
        test_plans_list = []
        for complete_test_plan_dict in complete_test_plans_dict:
            self.base_selenium.LOGGER.info(' + Is {} article in active status?'.format(complete_test_plan_dict['Article Name']))
            if self.article_page.is_article_in_table(value=complete_test_plan_dict['Article Name']):
                self.base_selenium.LOGGER.info(' + Active.')
                test_plans_list.append(complete_test_plan_dict)
            else:
                self.base_selenium.LOGGER.info(' + Archived.')
        else:
            return {}
        
        return test_plans_list

    def get_active_tst_unit_with_material_type(self, search, material_type='Raw Material'):
        self.base_selenium.LOGGER.info(' + Get Test Unit with  type {} .'.format(search))
        self.test_unit_page.get_test_units_page()
        test_units = self.test_unit_page.search(search)
        test_units_dict = [self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit) for
                                    test_unit in test_units[:-1]]
        for test_unit_dict in test_units_dict:
            if test_unit_dict['Type'] == search and material_type in test_unit_dict['Material Type']:
                return test_unit_dict
        return {}
    
    # this function generates random order data and then redirectes the user to the order's page
    def get_random_order_data(self):
        self.base_selenium.LOGGER.info('Generate new random data to update the order with')
        self.article_page.get_articles_page()
        new_random_material_type = self.generate_random_string()
        new_article_data = self.article_page.create_new_article(material_type=new_random_material_type)
        
        new_material_type = new_article_data['material_type']
        new_article = new_article_data['name']
        self.base_selenium.LOGGER.info('Generate new article with article name: {}, and material type: {}'.format(new_article, new_material_type))

        self.test_plan.get_test_plans_page()
        new_testplan_name = self.test_plan.create_new_test_plan(material_type=new_material_type, article=new_article, test_unit='tuqual')
        testplan_testunits = self.test_plan.get_testunits_in_testplans(test_plan_name=new_testplan_name)
        self.base_selenium.LOGGER.info('Generate new test plan with name: {}, and test units {}'.format(new_testplan_name, testplan_testunits))

        basic_order_data = {
            'article_name':new_article,
            'material_type': new_material_type,
            'testplan': new_testplan_name,
            'testunits_in_testplan': testplan_testunits
        }

        self.base_selenium.LOGGER.info('Redirect to order\'s page')
        self.order_page.get_orders_page()
        return basic_order_data
