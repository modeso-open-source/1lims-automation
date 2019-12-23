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

    def test009_test_plan_duplicate(self):
        '''
        LIMS-3679
        Duplicate a test plan
        '''
        # get the maximum number given to the latest testplan
        latest_testplan_row_data = self.test_plan.get_the_latest_row_data()
        largest_number = latest_testplan_row_data['Test Plan No.']
        duplicated_test_plan_number = int(largest_number) + 1
        self.base_selenium.LOGGER.info('The duplicated testplan should have the number: {}'.format(duplicated_test_plan_number))        

        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        main_testplan_data, row_index = self.test_plan.select_random_table_row(element='test_plans:test_plans_table')
        testplan_number = main_testplan_data['Test Plan No.']
        self.base_selenium.LOGGER.info('Testplan number: {} will be duplicated'.format(testplan_number))

        self.base_selenium.LOGGER.info('Saving the child data of the main testplan')        
        main_testplan_childtable_data = self.test_plan.get_child_table_data(index=row_index)

        self.base_selenium.LOGGER.info('Duplicating testplan number: {}'.format(testplan_number))        
        self.test_plan.duplicate_selected_item()

        self.test_plan.duplicate_testplan(change=['name'])
        self.test_plan.sleep_small()

        duplicated_testplan_data, duplicated_testplan_childtable_data = self.test_plan.get_specific_testplan_data_and_childtable_data(filter_by='number', filter_text=duplicated_test_plan_number)
        data_changed = ['Test Plan No.', 'Test Plan Name', 'Version', 'Changed On', 'Changed By', 'Created On']
        main_testplan_data, duplicated_testplan_data = self.remove_unduplicated_data(data_changed=data_changed, first_element=main_testplan_data, second_element=duplicated_testplan_data)

        self.base_selenium.LOGGER.info('Asserting that the data is duplicated correctly')        
        self.assertEqual(main_testplan_childtable_data, duplicated_testplan_childtable_data)
        self.assertEqual(main_testplan_data, duplicated_testplan_data)