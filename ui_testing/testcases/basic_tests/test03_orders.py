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
        headers = [header.text for header in headers]
        headers = list(filter(lambda x: (x != ''), headers))
        analysis_index = headers.index('Analysis No.')
        self.order_page.archive_selected_orders()
        self.analyses_page.get_analyses_page()
        self.analyses_page.sleep_small()
        analysisNumberArr = order_row_array[analysis_index].split(',')
        for x in analysisNumberArr:
            print(x)
            rows = self.analyses_page.search(x)
            self.analyses_page.click_check_box(source=rows[0])
            self.analyses_page.archive_selected_analysis()
            self.analyses_page.clear_search()

        self.order_page.get_orders_page()
        self.order_page.sleep_large()
        self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        self.order_page.archive_selected_orders()









