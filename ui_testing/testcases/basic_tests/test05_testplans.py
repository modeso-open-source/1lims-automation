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

    def test001_test_plan_delete_testunit(self):
        '''
        LIMS-3504
        Testing deleting a test unit from testplan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.
        '''

        completed_test_plans = self.test_plan_api.get_completed_testplans()
        testplan_name = random.choice(completed_test_plans)['testPlanName']

        # navigate to the chosen testplan edit page
        self.test_plan.get_test_plan_edit_page(testplan_name)

        # navigate to the testunits selection tab [Test plan create or update step 2] and get the testunits
        self.test_plan.navigate_to_testunits_selection_page()
        self.test_plan.switch_test_units_to_row_view()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()

        # get the name of the first testunit, which is the one to be deleted
        deleted_test_unit = (all_testunits[0])[0]

        # delete the first testunit
        self.test_plan.delete_the_first_testunit_from_the_tableview()

        # save the changes
        self.test_plan.save_and_confirm_popup()

        # refresh the page to make sure the changes were saved correctly
        self.base_selenium.LOGGER.info('Refreshing the page')
        self.base_selenium.refresh()
        self.test_plan.sleep_small()

        self.test_plan.navigate_to_testunits_selection_page()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()

        # checking if the data was saved correctly
        self.base_selenium.LOGGER.info('Checking if the changes were saved successfully')
        deleted_test_unit_found = self.test_plan.check_if_deleted_testunit_is_available(all_testunits=all_testunits, deleted_test_unit=deleted_test_unit)
        
        self.assertFalse(deleted_test_unit_found)

    def test003_test_plan_inprogress_to_completed(self):
        '''
        LIMS-3502
        When the testplan status is converted from 'In-Progress' to 'Completed', no new version created
        '''
        in_progress_status = 'in progress'
        self.base_selenium.LOGGER.info('Searching for test plans with In Progress status')
        in_progress_testplans = self.test_plan.search(in_progress_status)

        if in_progress_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            in_progress_testplan = in_progress_testplans[0]
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=in_progress_testplan)
            in_progress_testplan_name = row_data['Test Plan Name']
            in_progress_testplan_version = row_data['Version']
            self.base_selenium.LOGGER.info('Navigating to edit page of testplan: {} with version: {}'.format(in_progress_testplan_name, in_progress_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=in_progress_testplan_name)
            
            # go to step 2 and add testunit
            self.base_selenium.LOGGER.info('Going to step 2 to add testunit to this test plan')
            self.test_plan.set_test_unit()
            self.base_selenium.LOGGER.info('Saving and completing the testplan')
            self.test_plan.save(save_btn='test_plan:save_and_complete')

            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            testplan = self.test_plan.search(in_progress_testplan_name)[0]
            testplan_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testplan)
            completed_testplan_version = testplan_row_data['Version']
            
            self.assertEqual(in_progress_testplan_version, completed_testplan_version)
            self.assertEqual(testplan_row_data['Status'], 'Completed')