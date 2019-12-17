from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re, random


class TestPlansTestCases(BaseTest):
    # testplan = '';
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info('Getting the testplans page')
        self.test_plan.get_test_plans_page()


    # @skip('https://modeso.atlassian.net/browse/LIMS-3504')
    def test001_test_plan_delete_testunit(self):
        '''
        LIMS-3504
        Testing deleting a test unit from testplan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.
        '''
        # choose a random table row and navigate to its edit page
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_name = row_data['Test Plan Name']
        self.test_plan.get_test_plan_edit_page(testplan_name)

        # navigate to the testunits selection tab [Test plan create or update step 2]
        self.base_selenium.click(element='test_plan:testunits_selection')
        self.test_plan.sleep_small()

        self.base_selenium.click(element='test_plan:table_card_switcher')

        rows = self.base_selenium.get_table_rows(element='test_plan:testunits_table')
        old_length = len(rows)
        row_data = self.base_selenium.get_row_cells(rows[0])
        deleted_test_unit = row_data[0].text

        self.base_selenium.click(element='test_plan:row_delete_button')
        self.test_plan.sleep_medium()
        self.base_selenium.click(element='test_plan:save_btn')
        self.test_plan.sleep_small()
        self.base_selenium.click(element='test_plan:ok')
        self.test_plan.sleep_small()
        self.base_selenium.refresh()

        self.base_selenium.click(element='test_plan:testunits_selection')
        self.test_plan.sleep_small()

        rows = self.base_selenium.get_table_rows(element='test_plan:testunits_table')
        new_length = len(rows)
        deleted_test_unit_found = 0
        for row in rows:
            row_data = self.base_selenium.get_row_cells(row)
            if (row_data[0].text == deleted_test_unit):
                deleted_test_unit_found = 1

        self.assertTrue((new_length + 1 == old_length and not deleted_test_unit_found))
        self.test_plan.sleep_large()
        return


