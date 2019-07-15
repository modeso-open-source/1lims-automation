from unittest import TestCase
from ui_testing.pages.base_selenium import BaseSelenium
from uuid import uuid4
from ui_testing.pages.analyses_page import Analyses
from ui_testing.pages.article_page import Article
from ui_testing.pages.login_page import Login
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.testplan_page import TstPlan
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



