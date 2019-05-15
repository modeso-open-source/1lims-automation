from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TestPlan
from ui_testing.pages.order_page import Order
from ui_testing.pages.analyses_page import  Analyses

class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Article()
        self.test_plan = TestPlan()
        self.order_page = Order()
        self.analyses_page = Analyses()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

    def test01_archiveOrder(self):

        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        order_row_array = order_row.text.split('\n')

        headers = self.order_page.table_headers()
        headers = list(filter(lambda x: (x != ''), [header.text for header in headers]))
        analysis_index = headers.index('Analysis No.')
        analysis_numbers_array = order_row_array[analysis_index].split(',')

        order_deleted = self.order_page.archive_selected_orders()
        self.analyses_page.get_analyses_page()
        self.order_page.sleep_medium()

        if order_deleted:
           has_active_analysis = self.analyses_page.search_if_analysis_not_deleted(analysis_numbers_array)
           self.assertFalse(has_active_analysis)
        else:
            self.analyses_page.search_by_number_and_archive(analysis_numbers_array)
            self.order_page.get_orders_page()
            self.order_page.sleep_medium()
            rows = self.order_page.search(analysis_numbers_array[0])
            self.order_page.click_check_box(source=rows[0])
            self.order_page.archive_selected_orders()
            self.assertEqual(self.base_selenium.get_text(element='general:alert_confirmation'), 'Successfully Archived')










