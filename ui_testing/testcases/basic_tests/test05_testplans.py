from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re, random
from selenium.common.exceptions import NoSuchElementException        


class TestPlansTestCases(BaseTest):

    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

    def test005_archive_restore_test_plan(self):
        '''
        LIMS-3506
        '''

        # archive
        self.base_selenium.LOGGER.info('Choosing a random testplan table row to edit')
        # choose a random table row and navigate to its edit page
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        print(testplan_number)
        self.test_plan.sleep_small()
        print(row)
        self.test_plan.click_check_box(source=row)
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:archive')
        self.test_plan.sleep_small()
        self.test_plan.confirm_popup()
        self.test_plan.sleep_small()

        # self.test_plan.sleep_small()
        # self.test_plan.click_check_box(source=row)
        # self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:archived')
        self.test_plan.sleep_small()
        # self.base_selenium.click(element='test_plans:archive')
        # self.test_plan.sleep_small()
        # self.test_plan.confirm_popup()
        # self.test_plan.sleep_small()
        # self.confirm_popup()


        # restore
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        r = self.test_plan.search(testplan_number)
        # print(r[0].text)
        self.test_plan.sleep_small()
       
        self.test_plan.click_check_box(source=r[0])
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:restore')
        self.test_plan.sleep_small()
        self.test_plan.confirm_popup()
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:active')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plans:right_menu')
        self.test_plan.sleep_small()
        r = self.test_plan.search(testplan_number)
        print(r[0].text)
        self.test_plan.sleep_small()
