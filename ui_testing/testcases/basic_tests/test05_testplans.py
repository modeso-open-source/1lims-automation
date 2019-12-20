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
        self.base_selenium.LOGGER.info(' * Comparing the testplan no. {} '.format(testplan_number))
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