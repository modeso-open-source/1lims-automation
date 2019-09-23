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
        row = self.test_unit_page.get_random_test_units_row()
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

    def test004_check_version_after_update(self):
        """
        After I update any field then press on save , new version created in the active table.
        LIMS-3676
        After the user edit any of the followings fields
        test unit name
        test unit number
        category
        method
        iteration
        materiel type
        specification
        the should updated successfully when I enter one more time
        LIMS-5288
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        new_random_number = self.generate_random_number(upper=100000)
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()
        new_random_iteration = self.generate_random_number(upper=4)

        self.base_selenium.LOGGER.info('Getting data of the first testunit')
        testunits_records = self.test_unit_page.result_table()
        first_testunit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testunits_records[0])

        old_version = first_testunit_data['Version']
        self.base_selenium.LOGGER.info('old version: {}'.format(old_version))
        self.base_selenium.LOGGER.info('Open the first record to update it')
        self.test_unit_page.get_random_x(row=testunits_records[0])

        self.base_selenium.LOGGER.info('Set the new testunit number to be: {}'.format(new_random_number))
        self.test_unit_page.set_testunit_number(number=new_random_number)

        self.base_selenium.LOGGER.info('Set the new testunit name to be: {}'.format(new_random_name))
        self.test_unit_page.set_testunit_name(name=new_random_name)

        self.base_selenium.LOGGER.info('Set new material type')
        self.test_unit_page.set_material_type()
        new_materialtypes = self.test_unit_page.get_material_type()

        self.base_selenium.LOGGER.info('Set the new category to be: {}'.format(new_random_category))
        self.test_unit_page.set_category(category=new_random_category)

        self.base_selenium.LOGGER.info('Set the new testunit iteartions to be: {}'.format(new_random_iteration))
        self.test_unit_page.set_testunit_iteration(iteration=new_random_iteration)

        self.base_selenium.LOGGER.info('Set the method to be: {}'.format(new_random_method))
        self.test_unit_page.set_method(method=new_random_method)

        self.base_selenium.LOGGER.info('pressing save and create new version')
        self.test_unit_page.save_and_create_new_version(confirm=True)

        self.base_selenium.LOGGER.info('Refresh to make sure that the new data are saved')
        self.base_selenium.refresh()
        self.test_unit_page.sleep_small()

        self.base_selenium.LOGGER.info('Getting testunit data after referesh')
        updated_testunit_name = self.test_unit_page.get_testunit_name()
        update_testunit_number = self.test_unit_page.get_testunit_number()
        updated_material_types = self.test_unit_page.get_material_type()
        updated_category = self.test_unit_page.get_category()
        updated_iterations = self.test_unit_page.get_testunit_iteration()
        updated_method = self.test_unit_page.get_method()

        self.base_selenium.LOGGER.info(
            '+ Assert testunit name is: {}, and should be {}'.format(new_random_name, updated_testunit_name))
        self.assertEqual(new_random_name, updated_testunit_name)

        self.base_selenium.LOGGER.info(
            '+ Assert testunit number is: {}, and should be {}'.format(str(new_random_number), update_testunit_number))
        self.assertEqual(str(new_random_number), update_testunit_number)

        self.base_selenium.LOGGER.info(
            '+ Assert testunit materialTypes are: {}, and should be {}'.format(new_materialtypes,
                                                                               updated_material_types))
        self.assertEqual(new_materialtypes, updated_material_types)

        self.base_selenium.LOGGER.info(
            '+ Assert testunit category is: {}, and should be {}'.format(new_random_category, updated_category))
        self.assertEqual(new_random_category, updated_category)

        self.base_selenium.LOGGER.info(
            '+ Assert testunit iterations is: {}, and should be {}'.format(str(new_random_iteration),
                                                                           updated_iterations))
        self.assertEqual(str(new_random_iteration), updated_iterations)

        self.base_selenium.LOGGER.info(
            '+ Assert testunit Method is: {}, and should be {}'.format(new_random_method, updated_method))
        self.assertEqual(new_random_method, updated_method)

        self.test_unit_page.get_test_units_page()
        testunit_records = self.test_unit_page.result_table()
        first_testunit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testunit_records[0])
        new_version = first_testunit_data['Version']
        self.base_selenium.LOGGER.info(
            '+ Assert testunit version is: {}, new version: {}'.format(old_version, new_version))
        self.assertNotEqual(old_version, new_version)

    def test005_quantative_mibi_not_entering_dash_in_upper_limit(self):

        """
        Upper limit Approach, user can't enter  in the upper limit
        LIMS-3768
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with Quantitative MiBi and random generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type='Quantitative MiBi',
                                                method=new_random_method, upper_limit='-')

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info(
            'Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            '+ Assert error msg which indicates that it does not allow to add - in upper limit has appeared? {}'.format(
                validation_result))
        self.assertEqual(validation_result, True)

    @parameterized.expand(['spec', 'quan'])
    def test007_allow_unit_field_to_be_optional(self, specification_type):
        """
        Make sure the unit field of the specification or limit of quantification is an optional field.
        LIMS-4161
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_iteration = self.generate_random_number(lower=1, upper=4)
        new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)

        self.base_selenium.LOGGER.info('Create new testunit with the randomly generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type='Quantitative',
                                                iteration=new_random_iteration, method=new_random_method,
                                                spec_or_quan=specification_type, upper_limit=new_random_upper_limit)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info(
            'Search by testunit name: {}, to make sure that testunit created successfully'.format(new_random_name))
        test_unit = self.test_unit_page.search(value=new_random_name)[0]
        self.test_unit_page.get_random_x(test_unit)

        self.base_selenium.LOGGER.info(
            'Getting values of the unit field and upper limit to make sure that values saved correctly')
        if specification_type == 'spec':
            unit_value = self.test_unit_page.get_spec_unit()
            upper_limit_value = self.test_unit_page.get_spec_upper_limit()
        else:
            unit_value = self.test_unit_page.get_quan_unit()
            upper_limit_value = self.test_unit_page.get_quan_upper_limit()

        self.base_selenium.LOGGER.info('+ Assert unit value after save is: {}, and should be empty'.format(unit_value))
        self.assertEqual(unit_value, '')

        self.base_selenium.LOGGER.info('Checking with upper limit to make sure that data saved normally')
        self.assertEqual(upper_limit_value, str(new_random_upper_limit))

    @parameterized.expand(['spec', 'quan'])
    def test008_force_use_to_choose_specification_or_limit_of_quantification(self, specification_type):
        """
        The specification & Limit of quantification one of them should be mandatory.

        LIMS-4158
        """
        self.base_selenium.LOGGER.info('Prepare random data for the new testunit')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_iteration = self.generate_random_number(lower=1, upper=4)
        new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)

        self.base_selenium.LOGGER.info('Create new testunit with the randomly generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type='Quantitative',
                                                iteration=new_random_iteration, method=new_random_method)
        self.test_unit_page.sleep_tiny()
        self.base_selenium.LOGGER.info('Create new testunit with the random data')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info(
            'Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Checking that a validation message actually appeared which means that user can not create testunit without choosing specification of limit of quantification')
        self.assertEqual(validation_result, True)

        self.base_selenium.LOGGER.info('Set the testunit to be: {}'.format(specification_type))
        self.test_unit_page.use_specification_or_quantification(type_to_use=specification_type)

        if specification_type == 'spec':
            self.test_unit_page.set_spec_upper_limit(value=new_random_upper_limit)
        elif specification_type == 'quan':
            self.test_unit_page.set_quan_upper_limit(value=new_random_upper_limit)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info(
            'Search by testunit name: {}, to make sure that testunit created successfully'.format(new_random_name))
        self.test_unit_page.search(value=new_random_name)

        self.base_selenium.LOGGER.info('Getting records count')
        testunits_count = self.test_unit_page.get_table_records()

        self.base_selenium.LOGGER.info(
            '+ Assert testunit records count is: {}, and it should be {}'.format(testunits_count, 1))
        self.assertEqual(testunits_count, 1)

    @parameterized.expand(['Qualitative', 'Quantitative MiBi'])
    def test009_qualitative_value_should_be_mandatory_field(self, testunit_type):

        """
        The qualitative value should be mandatory field in the qualitative type

        LIMS-3766
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with Quantitative MiBi and random generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type=testunit_type,
                                                method=new_random_method)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info('Assert error msg')
        self.assertEqual(validation_result, True)

    @parameterized.expand(['Qualitative', 'Quantitative MiBi'])
    def test010_material_type_approach(self, testunit_type):
        """"
        In case I created test unit with 4 materiel type, when I go to test plan I should found that each test unit
         displayed according to it's materiel type.

         LIMS-3683

        """

        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.base_selenium.LOGGER.info(f'Create new testunit with {testunit_type} and random generated data')
        if testunit_type == 'Qualitative':
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method)
        else:
            new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)
            self.test_unit_page.create_quantitative_mibi_testunit(name=new_random_name, method=new_random_method,
                                                                  upper_limit=new_random_upper_limit)

        self.base_selenium.LOGGER.info('Set random n material type')
        for _ in range(3):
            self.test_unit_page.set_material_type()

        material_types = [material_type.replace('×', '') for material_type in self.test_unit_page.get_material_type()]

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        test_units = self.test_unit_api.get_all_test_units().json()['testUnits']

        for test_unit in test_units:
            if test_unit['name'] == new_random_name:
                for material_type in material_types:
                    self.assertIn(material_type, test_unit['materialTypes'])
                break
        else:
            self.fail('Material type is not there')
