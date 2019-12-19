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

    def test004_test_plan_completed_to_completed(self):
        '''
        LIMS-3501
        When the testplan status is converted from completed to completed a new version is created
        '''

        self.base_selenium.LOGGER.info('Searching for test plans with Completed status')
        completed_testplans = self.get_completed_testplans()

        if completed_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            completed_testplan = completed_testplans[0]
            old_completed_testplan_name = completed_testplan['testPlanName']
            old_completed_testplan_version = completed_testplan['version']
            self.base_selenium.LOGGER.info('Navigating to edit page of testplan: {} with version: {}'.format(old_completed_testplan_name, old_completed_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=old_completed_testplan_name)

            # go to step 2 and add testunit
            self.base_selenium.LOGGER.info('Going to step 2 to add testunit to this test plan')
            self.test_plan.set_test_unit(test_unit='a')
            self.test_plan.save_and_confirm_popup()
            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            testplan = self.test_plan.search(old_completed_testplan_name)[0]
            testplan_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testplan)
            completed_testplan_version = testplan_row_data['Version']

            self.assertEqual(old_completed_testplan_version + 1, int(completed_testplan_version))
            self.assertEqual(testplan_row_data['Status'], 'Completed')

        return  
