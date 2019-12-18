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
        # self.base_selenium.LOGGER.info('Getting the testplans page')
        self.test_plan.get_test_plans_page()

    # @skip('https://modeso.atlassian.net/browse/LIMS-3501')
    def test004_test_plan_completed_to_completed(self):
        '''
        LIMS-3501
        When the testplan status is converted from completed to completed a new version is created
        '''
        completed_status = 'completed'
        self.base_selenium.LOGGER.info('Searching for test plans with Completed status')
        completed_testplans = self.test_plan.search(completed_status)

        if completed_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            completed_testplan = completed_testplans[0]
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=completed_testplan)
            old_completed_testplan_name = row_data['Test Plan Name']
            old_completed_testplan_version = row_data['Version']
            self.base_selenium.LOGGER.info('Navigating to edit page of testplan: {} with version: {}'.format(old_completed_testplan_name, old_completed_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=old_completed_testplan_name)

            # go to step 2 and add testunit
            self.base_selenium.LOGGER.info('Going to step 2 to add testunit to this test plan')
            self.test_plan.set_test_unit()
            self.test_plan.save(save_btn='test_plan:save')

            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            testplan = self.test_plan.search(old_completed_testplan_name)[0]
            testplan_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testplan)
            completed_testplan_version = testplan_row_data['Version']

            self.assertEqual(old_completed_testplan_version + 1, completed_testplan_version)
            self.assertEqual(testplan_row_data['Status'], 'Completed')

        return  
