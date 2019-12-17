from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re, random
from selenium.common.exceptions import NoSuchElementException        


class TestPlansTestCases(BaseTest):
    # testplan = '';
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        # self.base_selenium.LOGGER.info('Getting the testplans page')
        self.test_plan.get_test_plans_page()


    # @skip('https://modeso.atlassian.net/browse/LIMS-3504')
    def test001_test_plan_delete_testunit(self):
        '''
        LIMS-3504
        Testing deleting a test unit from testplan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.
        '''

        testplan_notfound = 1
        rows = []
        old_length = 0
        row_data = None

        while (testplan_notfound):
            self.base_selenium.LOGGER.info('Choosing a random testplan table row to edit')
            # choose a random table row and navigate to its edit page
            row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
            testplan_name = row_data['Test Plan Name']
            self.test_plan.sleep_small()

            # navigate to the chosen testplan edit page
            self.test_plan.get_test_plan_edit_page(testplan_name)

            # navigate to the testunits selection tab [Test plan create or update step 2]
            self.test_plan.navigate_to_testunits_selection_page()

            try:
                # switch to table view
                self.base_selenium.LOGGER.info('Switching from card view to table view')
                self.base_selenium.click(element='test_plan:table_card_switcher')
            except NoSuchElementException: # already in the table view
                self.base_selenium.LOGGER.info('Already in the table view')

            # get all the testunits from the table view
            rows = self.test_plan.get_all_testunits_in_testplan()
            old_length = len(rows)

            # get the name of the first testunit, which is the one to be deleted
            row_data = self.base_selenium.get_row_cells(rows[0])
            if (old_length > 1 or row_data[0].text != 'No Results Found'):
                testplan_notfound = 0

            if (testplan_notfound):
                self.base_selenium.LOGGER.info('No testunits found for this testplan')
                self.base_selenium.LOGGER.info('Redirecting to the testplans active table')
                self.test_plan.get_test_plans_page()

        deleted_test_unit = row_data[0].text

        # delete the first testunit
        self.test_plan.delete_the_first_testunit_from_the_tableview()

        # save the changes
        self.test_plan.save(save_btn='test_plan:save_btn')
        self.test_plan.sleep_small()

        # press 'Ok' on the popup
        self.base_selenium.LOGGER.info('Accepting the changes made')
        self.base_selenium.click(element='test_plan:ok')
        self.test_plan.sleep_small()

        # refresh the page to make sure the changes were saved correctly
        self.base_selenium.LOGGER.info('Refreshing the page')
        self.base_selenium.refresh()
        self.test_plan.sleep_small()

        self.test_plan.navigate_to_testunits_selection_page()

        rows = self.test_plan.get_all_testunits_in_testplan()
        new_length = len(rows)
        deleted_test_unit_found = 0

        # checking if the data was saved correctly
        self.base_selenium.LOGGER.info('Checking if the changes were saved successfully')
        for row in rows:
            row_data = self.base_selenium.get_row_cells(row)
            if ((row_data[0].text == deleted_test_unit) or ((new_length == old_length) and (row_data[0].text != 'No Results Found'))):
                deleted_test_unit_found = 1
            
        self.assertFalse(deleted_test_unit_found)
        return


