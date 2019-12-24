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

    def test007_exporting_test_plan_one_record(self):
        '''
        LIMS-3508 Case 1
        Exporting one record
        '''
        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplan number: {} will be exported'.format(testplan_number))
        
        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=row)
        self.test_plan.sleep_small()

        self.test_plan.download_xslx_sheet()

        row_data_list = list(row_data.values())
        self.base_selenium.LOGGER.info('Comparing the testplan no. {} '.format(testplan_number))
        values = self.test_plan.sheet.iloc[0].values
        fixed_sheet_row_data = self.fix_data_format(values)
        for item in row_data_list:
            if item != '' and item != '-':
                self.assertIn(item, fixed_sheet_row_data)
        
    def test008_exporting_test_plan_multiple_records(self):
        '''
        LIMS-3508 Case 2
        Exporting multiple records
        '''
        self.base_selenium.LOGGER.info('Choosing random multiple testplans table rows')
        rows = self.test_plan.select_random_multiple_table_rows(element='test_plans:test_plans_table')
        testplan_rows = rows[0]
        testplans_numbers = []
        for row in testplan_rows:
            testplans_numbers.append(row['Test Plan No.'])
        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplans numbers: {} will be exported'.format(testplans_numbers))

        self.test_plan.download_xslx_sheet()

        row_data_list = []
        for row_data in testplan_rows:
            row_data_list.append(list(row_data.values()))
        
        self.base_selenium.LOGGER.info('Comparing the testplan no. {} '.format(testplans_numbers))
        row_data_list = sorted(row_data_list, key=lambda x: x[1], reverse=True)

        for index in range(len(row_data_list)):
            fixed_row_data = self.fix_data_format(row_data_list[index])
            values = self.test_plan.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item != '' and item != '-':
                    self.assertIn(item, fixed_sheet_row_data)