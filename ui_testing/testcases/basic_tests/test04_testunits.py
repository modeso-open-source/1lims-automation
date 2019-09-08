from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_unit_page.get_test_units_page()

    @skip('https://modeso.atlassian.net/browse/LIMS-5237')
    def test001_test_units_search(self):
        """
        New: Test units: Search Approach: I can search by any field in the table view

        LIMS-3674
        :return:
        """
        row= self.test_unit_page.get_random_test_units_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test002_archive_test_units(self):
        """
        New: Test units: Archive Approach: I can archive any test unit successfully.

        LIMS-3670
        :return:
        """
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        self.test_unit_page.archive_selected_test_units()
        self.test_unit_page.get_archived_test_units()
        for test_unit in selected_test_units_data:
            test_unit_name = test_unit['Test Unit Name']
            self.base_selenium.LOGGER.info(' + {} Test Unit should be activated.'.format(test_unit_name))
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))

    def test003_restore_test_units(self):
        """
         New: Test units: Restore Approach: I can restore any test unit successfully.

        LIMS-5262
        :return:
        """
        test_unit_names = []
        self.test_unit_page.get_archived_test_units()
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        for test_unit in selected_test_units_data:
            test_unit_names.append(test_unit['Test Unit Name'])

        self.test_unit_page.restore_selected_test_units()
        self.test_unit_page.get_active_test_units()
        for test_unit_name in test_unit_names:
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))

    @parameterized.expand(['spec', 'quan'])
    def test008_force_use_to_choose_specification_or_limit_of_quantification (self, specificationType):
        """
        The specification & Limit of quantification one of them should be mandatory.

        LIMS-4158
        """
        self.base_selenium.LOGGER.info('Prepare random data for the new testunit')
        newRandomName = self.generate_random_string()
        newRandomMethod = self.generate_random_string()
        newRandomCategry = self.generate_random_string()
        newRandomIterations = self.generate_random_number(limit=4)
        newRandomUpperLimit = self.generate_random_number(limit=1000)

        self.base_selenium.LOGGER.info('Create new testunit with the randomly generated data')
        self.test_unit_page.create_new_testunit(name=newRandomName, testunitType='Quantitative', iteration=newRandomIterations, method=newRandomMethod)

        self.base_selenium.LOGGER.info('Sleep to make sure that page is loaded')
        self.test_unit_page.sleep_tiny()

        self.base_selenium.LOGGER.info('Create new testunit with the random data')
        self.test_unit_page.save(save_btn='general:saveForm', loggerMsg='Save new testunit')
        
        self.base_selenium.LOGGER.info('Sleep to make sure that data is written to be ready for validation')
        self.test_unit_page.sleep_tiny()

        self.base_selenium.LOGGER.info('Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result =  self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info('Checking that a validation message actually appeared which means that user can not create testunit without choosing specification of limit of quantification')
        self.assertEqual(validation_result, True)
        
        self.base_selenium.LOGGER.info('Set the testunit to be: {}'.format(specificationType))
        self.test_unit_page.use_specification_or_quantification(typeToUse=specificationType)

        if specificationType == 'spec':
            self.test_unit_page.set_spec_upper_limit(value=newRandomUpperLimit)
        elif specificationType == 'quan':
            self.test_unit_page.set_quan_upper_limit(value=newRandomUpperLimit)

        self.test_unit_page.sleep_tiny()
        
        self.test_unit_page.save(save_btn='general:saveForm', loggerMsg='Save new testunit')

        self.base_selenium.LOGGER.info('Search by testunit name: {}, to make sure that testunit created successfully'.format(newRandomName))
        self.test_unit_page.search(value=newRandomName)

        self.base_selenium.LOGGER.info('Getting records count')
        testunits_count = self.order_page.get_table_records()

        self.base_selenium.LOGGER.info('+ Assert testunit records count is: {}, and it should be {}'.format(testunits_count, 1))
        self.assertEqual(testunits_count, 1)





        
