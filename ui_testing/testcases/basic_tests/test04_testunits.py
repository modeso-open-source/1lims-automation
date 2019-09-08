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
    def test007_allow_unit_field_to_be_optional (self, specificationType):
        """
        Make sure the unit field of the specification or limit of quantification is an optional field.

        LIMS-4161
        """
        self.base_selenium.LOGGER.info('Generate random upper limit to be used in filling data')
        randomUpperLimit = self.generate_random_number(limit=500)

        self.base_selenium.LOGGER.info('Filter by type Qualitative')
        self.test_unit_page.search(value='Qualitative')

        self.base_selenium.LOGGER.info('Open random record')
        randomTestunitRecord = self.test_unit_page.get_random_table_row(table_element='general:table')
        self.test_unit_page.get_random_x(row = randomTestunitRecord)

        self.base_selenium.LOGGER.info('Set the testunit type to be quantitative so i can choose whether it has limit of quantification or specification or both')
        self.test_unit_page.set_testunit_type(testunitType='Quantitative')

        self.base_selenium.LOGGER.info('Set testunit to use {}'.format(specificationType))
        self.test_unit_page.use_specification_or_quantification(typeToUse=specificationType)

        if specificationType == 'spec':
            self.base_selenium.LOGGER.info('Setting the upper limit value in in upper limit field')
            self.test_unit_page.set_spec_upper_limit(value=randomUpperLimit)

            self.base_selenium.LOGGER.info('Setting unit value to be empty')
            self.test_unit_page.set_spec_unit(value='')
        else:
            self.base_selenium.LOGGER.info('Setting the upper limit value in in upper limit field')
            self.test_unit_page.set_quan_upper_limit(value=randomUpperLimit)

            self.base_selenium.LOGGER.info('Setting unit value to be empty')
            self.test_unit_page.set_quan_unit(value='')

        self.base_selenium.LOGGER.info('Sleeping for a tiny time to make sure that values are set to take place in validation')
        self.test_unit_page.sleep_tiny()

        self.base_selenium.LOGGER.info('pressing save and create new version')
        self.test_unit_page.saveAndCreateNewVersion(confirm=True)

        self.base_selenium.LOGGER.info('Refresh to make sure that the new data are saved')
        self.base_selenium.refresh()
        self.test_unit_page.sleep_small()

        self.base_selenium.LOGGER.info('Setting random upper limit text in the variable to make sure that the field actually has no value')
        unitValue = 'test text'
        upperLimitValue = -445

        self.base_selenium.LOGGER.info('Getting values of the unit field and upper limit to make sure that values saved correctly')
        if specificationType == 'spec':
            unitValue = self.test_unit_page.get_spec_unit()
            upperLimitValue = self.test_unit_page.get_spec_upper_limit()
        else:
            unitValue = self.test_unit_page.get_quan_unit()
            upperLimitValue = self.test_unit_page.get_quan_upper_limit()
            
        self.base_selenium.LOGGER.info('+ Assert unit value after save is: {}, and should be empty'.format(unitValue))
        self.assertEqual(unitValue, '')

        self.base_selenium.LOGGER.info('Checking with upper limit to make sure that data saved normally')
        self.base_selenium.LOGGER.info('+ Assert upper limit value after save is: {}, and should be: {}'.format(upperLimitValue, randomUpperLimit))
        self.assertEqual(upperLimitValue, str(randomUpperLimit))
