from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.articles_page import Articles
from unittest import skip
from parameterized import parameterized
import re, random


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.articles_page = Articles()
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
        self.test_unit_page.open_edit_page(row=testunits_records[0])

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

        self.base_selenium.LOGGER.info('Getting testunit data after refresh')
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

    def test006_search_by_archived_testunit(self):
        """
        Archived test units shouldn't display in the test plan step two & also in the analysis step two.
        LIMS-3677
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        material_type='All')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Search by the testunit name {} to archive'.format(new_random_name))
        self.test_unit_page.search(value=new_random_name)

        self.base_selenium.LOGGER.info('Archive the testunit')
        self.test_unit_page.select_random_multiple_table_rows()
        self.test_unit_page.archive_selected_test_units()

        self.base_selenium.LOGGER.info('Get testplans page')
        self.test_plan.get_test_plans_page()

        self.base_selenium.LOGGER.info('Get first record in testplans page')
        testplans_records = self.test_plan.result_table()
        self.test_plan.open_edit_page(row=testplans_records[0])

        self.base_selenium.click('test_plan:next')
        self.base_selenium.click('test_plan:add_test_units')
        self.base_selenium.LOGGER.info('Assert that archived test unit is not existing')
        self.assertFalse(
            self.base_selenium.is_item_in_drop_down(element='test_plan:test_units', item_text=new_random_name))

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
        self.test_unit_page.open_edit_page(test_unit)

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

        self.base_selenium.LOGGER.info('Create new testunit with {} and random generated data'.format(testunit_type))
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

    @parameterized.expand([(True,), (False,)])
    def test011_create_test_unit_with_random_category(self, random):
        """
        User can create test unit with an random category

        LIMS-3682
        """
        self.base_selenium.LOGGER.info("Create new test unit with random:{} category".format(random))
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string() if random else ""
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        category=new_random_category)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the category of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]
        self.test_unit_page.open_edit_page(test_unit)

        category = self.test_unit_page.get_category()
        self.base_selenium.LOGGER.info('Assert category : {}'.format(category))
        self.assertEqual(new_random_category, category) if random else self.assertTrue(category)

    @parameterized.expand([('upper', 'spec'),
                           ('upper', 'quan'),
                           ('lower', 'spec'),
                           ('lower', 'quan')
                           ])
    def test012_create_test_unit_with_one_limit_only(self, limit, spec_or_quan):
        """
        New: Test unit: Specification Approach: In case I entered the upper limit or the lower limit only,
         the specification should display <=or >= according to that in the table view.

        LIMS-3681
        LIMS-4415
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_limit = self.generate_random_number(lower=500, upper=1000)

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        if limit == "upper":
            self.base_selenium.LOGGER.info('Create with upper limit : {} & {} '.format(new_random_limit, spec_or_quan))
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             upper_limit=new_random_limit, spec_or_quan=spec_or_quan)
        else:
            self.base_selenium.LOGGER.info('Create with lower limit : {} & {} '.format(new_random_limit, spec_or_quan))
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             lower_limit=new_random_limit, spec_or_quan=spec_or_quan)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]
        test_unit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit)
        specifications = test_unit_data['Specifications']
        quantification_limit = test_unit_data['Quantification Limit']

        if limit == "upper":
            self.base_selenium.LOGGER.info('Check that <= is existing in {}'.format(spec_or_quan))
            self.assertIn('<=', specifications) if 'spec' in spec_or_quan else self.assertIn('<=', quantification_limit)
        else:
            self.base_selenium.LOGGER.info('Check that >= is existing in specifications')
            self.assertIn('>=', specifications) if 'spec' in spec_or_quan else self.assertIn('>=', quantification_limit)

    @parameterized.expand([('upper'), ('lower')])
    def test013_limits_of_quantification_approach(self, limit):
        """
        New: Test units : Limits of quantification Approach: In case I didn't enter empty values in the upper/lower
        limits of the specification of limits of quantification, it should display N/A in the active table


        LIMS:4427
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()
        new_random_limit = self.generate_random_number(lower=500, upper=1000)
        spec_or_quan = 'spec'

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        if limit == "upper":
            self.base_selenium.LOGGER.info('Create with upper limit : {} & {} '.format(new_random_limit, spec_or_quan))
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             upper_limit=new_random_limit, spec_or_quan=spec_or_quan,
                                                             category=new_random_category)
        else:
            self.base_selenium.LOGGER.info('Create with lower limit : {} & {} '.format(new_random_limit, spec_or_quan))
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             lower_limit=new_random_limit, spec_or_quan=spec_or_quan,
                                                             category=new_random_category)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]

        quantifications_limit = self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit)[
            'Quantification Limit']
        self.base_selenium.LOGGER.info('Check that N/A is existing in Quantification')
        self.assertIn('N/A', quantifications_limit)

    def test014_quantitative_mibi_type_allow_upper_limit_the_concentration_to_be_mandatory_fields(self):
        """
            Test unit: Specification Approach: In quantitative MiBi type allow upper
             limit & the concentration to be mandatory fields

        LIMS-3769
        LIMS-5287
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()
        new_random_limit = self.generate_random_number(lower=500, upper=1000)

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.base_selenium.LOGGER.info('Create with upper limit : {}'.format(new_random_limit))
        self.test_unit_page.create_quantitative_mibi_testunit(name=new_random_name, method=new_random_method,
                                                              upper_limit=new_random_limit,
                                                              category=new_random_category)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]
        self.test_unit_page.open_edit_page(test_unit)

        self.test_unit_page.clear_spec_upper_limit()
        self.test_unit_page.clear_cons()

        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit, should fail')

        self.base_selenium.LOGGER.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info('Assert error msg')
        self.assertEqual(validation_result, True)

    def test015_specification_limit_of_quantification_approach(self):
        """
        New: Test unit: Specification/limit of quantification Approach: Allow user to select those both options
        ( specification & limit of quantification ) at the same time ( create test unit with both selection )

        LIMS-4159
        :return:
        """

        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()
        new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)
        new_random_lower_limit = self.generate_random_number(lower=1, upper=500)
        spec_or_quan = 'spec_quan'

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                         upper_limit=new_random_upper_limit,
                                                         lower_limit=new_random_lower_limit,
                                                         spec_or_quan=spec_or_quan, category=new_random_category)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]
        test_unit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit)
        specifications = test_unit_data['Specifications']
        quantification_limit = test_unit_data['Quantification Limit']

        self.info('Assert upper and lower limits are in specifications')
        self.assertEqual("{}-{}".format(new_random_lower_limit, new_random_upper_limit), specifications)

        self.info('Assert upper and lower limits are in quantification_limit')
        self.assertEqual("{}-{}".format(new_random_lower_limit, new_random_upper_limit), quantification_limit)

    def test016_fields_of_the_specification_limits_of_quant_should_be_disabled_if_the_checkbox_is_not_selected(self):
        """
        The fields of the specification & limits of quantification should be  disabled if the checkbox is not selected

        LIMS-4418
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                         category=new_random_category, spec_or_quan="")
        self.info('Assert that all limits fields are not active')
        for limit in ['quan_upper', 'quan_lower', 'spec_upper', 'spec_lower']:
            class_attr = self.base_selenium.get_attribute('test_unit:{}_limit'.format(limit), 'class')
            self.info('Assert that {}_limit is not active'.format(limit))
            self.assertNotIn('ng-valid', class_attr)

    @parameterized.expand([('quan'), ('spec')])
    def test017_create_quantative_with_limits_of_quantative_only_and_specification_only(self):
        """
        New:Test unit: Create Approach: User can create test unit with limits of quantification type only &
        with upper lower limits
        New: Test unit: Creation Approach: User can create test units with Quantitative type with specification only
        LIMS-5427
        LIMS-4156
        :return:
        """

        new_name = self.generate_random_string()
        new_method = self.generate_random_string()
        new_random_limit = self.generate_random_number()

        self.test_unit_page.create_quantitative_testunit(name=new_name, material_type='', category='',
                                                         upper_limit=new_random_limit, lower_limit=new_random_limit,
                                                         spec_or_quan='quan', method=new_method)

        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')
        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_name)[0]
        self.test_unit_page.open_edit_page(test_unit)
        testunit_name = self.test_unit_page.get_testunit_name()
        self.base_selenium.LOGGER.info('Assert test unit name : {}'.format(testunit_name))
        self.assertEqual(new_name, testunit_name)

        new_name = self.generate_random_string()
        new_method = self.generate_random_string()
        new_random_limit = self.generate_random_number()

        self.test_unit_page.create_quantitative_testunit(name=new_name, material_type='', category='',
                                                         upper_limit=new_random_limit, lower_limit=new_random_limit,
                                                         spec_or_quan='spec', method=new_method)

        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')
        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_name)[0]
        self.test_unit_page.open_edit_page(test_unit)
        testunit_name = self.test_unit_page.get_testunit_name()
        self.base_selenium.LOGGER.info('Assert test unit name : {}'.format(testunit_name))
        self.assertEqual(new_name, testunit_name)

    @skip('https://modeso.atlassian.net/browse/LIMS-5525')
    def test019_download_test_units_sheet(self):
        """
        New: Test unit: Limit of quantification Approach: Allow those fields to displayed in table view &
        XSLX file ( upper limit & lower limit & unit )

        LIMS:4166
        LIMS-3672
        :return:
        """
        self.info(' * Download XSLX sheet')
        self.test_unit_page.download_xslx_sheet()
        rows_data = self.test_unit_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the test units with index : {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.test_unit_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            self.info(fixed_sheet_row_data)
            for item in fixed_row_data:
                if item == 'N/A' or str(item)[-3:] == '...':
                    continue
                self.assertIn(item, fixed_sheet_row_data)

    def test020_specification_limit_of_quantification_approach_can_be_minus(self):
        """
        New: Test unit: Quantitative: Specification Approach User can enter (-) in upper/lower limit

        LIMS-3767
        :return:
        """

        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()
        spec_or_quan = 'spec_quan'

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                         upper_limit="-", lower_limit="-",
                                                         spec_or_quan=spec_or_quan, category=new_random_category)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        test_unit = self.test_unit_page.search(new_random_name)[0]
        test_unit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=test_unit)
        specifications = test_unit_data['Specifications']

        self.info('Assert upper and lower limits are in specifications with N/A values')
        self.assertEqual("N/A", specifications)

    def test021_change_quantification_limits_not_effect_test_plan(self):
        """
        New: Test units/effect on test plan: Limits of quantification Approach: In case I make any edit in the limits
         of quantification, this shouldn't effect on test plan

         LIMS-4420
        :return:
        """
        active_articles_with_material_types = self.get_active_articles_with_material_type()
        material_type = next(iter(active_articles_with_material_types))
        article = active_articles_with_material_types[material_type][0]
        test_unit_new_name = self.generate_random_string()
        new_method = self.generate_random_string()
        new_random_limit = self.generate_random_number()

        self.test_unit_page.create_quantitative_testunit(name=test_unit_new_name, material_type=material_type,
                                                         upper_limit=new_random_limit, lower_limit=new_random_limit,
                                                         spec_or_quan='quan', method=new_method)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='save new testunit')

        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(name=test_unit_new_name, material_type=material_type,
                                            test_unit=test_unit_new_name, article=article, upper=100, lower=10)

        self.info('change upper limits of the test unut')
        self.test_unit_page.get_test_units_page()
        test_unit = self.test_unit_page.search(test_unit_new_name)[0]
        self.test_unit_page.open_edit_page(test_unit)

        self.test_unit_page.set_quan_upper_limit('10000')
        self.test_unit_page.set_quan_lower_limit('10000')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='save the changes')

        self.test_plan.get_test_plans_page()
        test_plan = self.test_plan.search(test_unit_new_name)[0]
        self.test_plan.open_edit_page(test_plan)

        upper, lower = self.test_plan.get_test_unit_limits()
        self.info('assert that limits have not changed')
        self.assertEqual(upper, '100')
        self.assertEqual(lower, '10')

    def test022_create_multi_test_units_with_same_name(self):
        """
        New: Test unit: Creation Approach; In case I create two test units with the same name,
        when I go to the test plan I found both of those with the same name

        LIMS-3684
        :return:
        """
        active_articles_with_material_types = self.get_active_articles_with_material_type()
        material_type = next(iter(active_articles_with_material_types))
        article = active_articles_with_material_types[material_type][0]
        test_unit_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        category = self.generate_random_string()

        self.test_unit_page.create_qualitative_testunit(name=test_unit_name, method=new_random_method,
                                                        material_type=material_type, category=category)
        self.test_unit_page.save(save_btn='general:save_form',
                                 logger_msg='save {} qualitative test unit'.format(test_unit_name))

        self.test_unit_page.create_quantitative_mibi_testunit(name=test_unit_name, method=new_random_method,
                                                              upper_limit=1000, material_type=material_type,
                                                              category=category)
        self.test_unit_page.save(save_btn='general:save_form',
                                 logger_msg='save {} quantitative_mibi test unit'.format(test_unit_name))

        self.test_unit_page.create_qualitative_testunit(name=test_unit_name, method=new_random_method,
                                                        material_type=material_type, category=category)
        self.test_unit_page.save(save_btn='general:save_form',
                                 logger_msg='save {} qualitative test unit'.format(test_unit_name))
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(name=test_unit_name, material_type=material_type, article=article)
        test_plan = self.test_plan.search(test_unit_name)[0]
        self.test_plan.open_edit_page(test_plan)
        self.base_selenium.click('test_plan:next')
        self.base_selenium.click('test_plan:add_test_units')
        test_units = self.base_selenium.get_drop_down_suggestion_list(element='test_plan:test_units',
                                                                      item_text=test_unit_name)

        self.info('assert that all test units are in the suggestions list')
        self.assertEqual(len(test_units), 3)

    def test023_duplicate_test_case(self):
        """"
        New: Test unit: Duplication Approach: I can duplicate the test unit with only one record

        LIMS-3678
        """
        random_test_unit = self.test_unit_page.select_random_table_row()
        test_unit_name = random_test_unit['Test Unit Name']
        self.info('test unit name : {}'.format(test_unit_name))
        old_test_units = len(self.test_unit_page.search(test_unit_name))
        self.test_unit_page.duplicate_test_unit()
        new_test_units = len(self.test_unit_page.search(test_unit_name))
        self.info('assert there is a new test unit')
        self.assertGreater(new_test_units, old_test_units)

    @parameterized.expand(['unitsub', 'unitsuper'])
    def test029_qualitative_test_unit_with_sub_and_super_scripts_appears_in_exported_sheet(self,
                                                                                           unit_with_sub_or_super):
        """
        New: Test unit: Export: Sub & Super scripts Approach: Allow user to see the sub & super scripts in the export file

        LIMS-5795
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        if unit_with_sub_or_super == 'unitsub':
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                            material_type='All',
                                                            unit=unit_with_sub_or_super.replace('sub', '[sub]'),
                                                            category=new_random_category)
        else:
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                            material_type='All',
                                                            unit=unit_with_sub_or_super.replace('super', '{super}'),
                                                            category=new_random_category)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        self.test_unit_page.search(new_random_name)
        self.test_unit_page.download_xslx_sheet()
        rows_data = self.test_unit_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.base_selenium.LOGGER.info(' * Comparing the unit name no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.test_unit_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item == unit_with_sub_or_super:
                    self.assertIn(item, fixed_sheet_row_data)

    @parameterized.expand(['unitsub', 'unitsuper'])
    def test031_create_qualitative_test_unit_with_sub_and_super_scripts(self, unit_with_sub_or_super):
        """

        Test unit : Unit: Subscript and superscript scripts Approach: Allow the unit filed to accept sub and super scripts in the test unit form

        LIMS-5784
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        if unit_with_sub_or_super == 'unitsub':
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                            material_type='All',
                                                            unit=unit_with_sub_or_super.replace('sub', '[sub]'),
                                                            category=new_random_category)
        else:
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                            material_type='All',
                                                            unit=unit_with_sub_or_super.replace('super', '{super}'),
                                                            category=new_random_category)

        self.test_unit_page.sleep_tiny()
        inserted_unit = self.test_unit_page.get_spec_unit()
        preview_unit = self.test_unit_page.get_spec_unit_preview()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        self.test_unit_page.search(new_random_name)
        rows_data = self.test_unit_page.get_table_rows_data()
        self.base_selenium.LOGGER.info(' * Comparing the unit name')
        fixed_row_data = self.fix_data_format(rows_data[0].split('\n'))
        self.assertIn(preview_unit, fixed_row_data)
        self.assertNotIn(inserted_unit, fixed_row_data)

    @parameterized.expand(['unitsub', 'unitsuper'])
    def test026_create_quantitative_test_unit_with_sub_and_super_scripts(self, unit_with_sub_or_super):
        """

        Test unit form: Unit accepts subscript and superscript characters in case of quantitative type with limit of quantification unit

        LIMS-5785
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with quantitative and random generated data')
        if unit_with_sub_or_super == 'unitsub':
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             material_type='All', upper_limit='33',
                                                             unit=unit_with_sub_or_super.replace('sub', '[sub]'),
                                                             category=new_random_category, lower_limit='22',
                                                             spec_or_quan='spec')
        else:
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             material_type='All', upper_limit='33',
                                                             unit=unit_with_sub_or_super.replace('super', '{super}'),
                                                             category=new_random_category, lower_limit='22',
                                                             spec_or_quan='spec')

        self.test_unit_page.sleep_tiny()
        inserted_unit = self.test_unit_page.get_spec_unit()
        preview_unit = self.test_unit_page.get_spec_unit_preview()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        self.test_unit_page.search(new_random_name)
        rows_data = self.test_unit_page.get_table_rows_data()
        self.base_selenium.LOGGER.info(' * Comparing the unit name')
        fixed_row_data = self.fix_data_format(rows_data[0].split('\n'))
        self.assertIn(preview_unit, fixed_row_data)
        self.assertNotIn(inserted_unit, fixed_row_data)

    @parameterized.expand(['unitsub', 'unitsuper'])
    def test027_quantitative_test_unit_with_sub_and_super_scripts_appears_in_exported_sheet(self,
                                                                                            unit_with_sub_or_super):
        """
        Test unit: Export: Sub & Super scripts Approach:  Allow user to see the sub & super scripts in the export file

        LIMS-5809
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        self.base_selenium.LOGGER.info('Create new testunit with quantitative and random generated data')
        if unit_with_sub_or_super == 'unitsub':
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             material_type='All', upper_limit='33',
                                                             unit=unit_with_sub_or_super.replace('sub', '[sub]'),
                                                             category=new_random_category, lower_limit='22',
                                                             spec_or_quan='spec')
        else:
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             material_type='All', upper_limit='33',
                                                             unit=unit_with_sub_or_super.replace('super', '{super}'),
                                                             category=new_random_category, lower_limit='22',
                                                             spec_or_quan='spec')

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')
        self.base_selenium.LOGGER.info('Get the test unit of it')
        self.test_unit_page.search(new_random_name)
        self.test_unit_page.download_xslx_sheet()
        rows_data = self.test_unit_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.base_selenium.LOGGER.info(' * Comparing the unit name no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.test_unit_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item == unit_with_sub_or_super:
                    self.assertIn(item, fixed_sheet_row_data)

    @parameterized.expand(['quantitative', 'qualitative'])
    def test028_create_test_unit_appears_in_version_table(self, unit_type):
        """

        New: Test unit: Versions Approach: After you create new record, all the columns should display in the version table

        LIMS-5289
        :return:
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_category = self.generate_random_string()

        if unit_type == 'quantitative':
            self.base_selenium.LOGGER.info('Create new testunit with quantitative and random generated data')
            self.test_unit_page.create_quantitative_testunit(name=new_random_name, method=new_random_method,
                                                             material_type='All', upper_limit='33',
                                                             unit='',
                                                             category=new_random_category, lower_limit='22',
                                                             spec_or_quan='spec')
        else:
            self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
            self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                            material_type='All',
                                                            unit='',
                                                            category=new_random_category)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get the test unit of it')
        self.test_unit_page.search(new_random_name)

        self.base_selenium.LOGGER.info('Open Versions for the newly created test unit')
        self.test_unit_page.get_versions_of_selected_test_units()
        rows_data = self.test_unit_page.get_table_rows_data()
        self.base_selenium.LOGGER.info(' * Comparing the unit name and method')
        fixed_row_data = self.fix_data_format(rows_data[0].split('\n'))
        self.assertIn(new_random_name, fixed_row_data)
        self.assertIn(new_random_method, fixed_row_data)

    @parameterized.expand(['ok', 'cancel'])
    def test024_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.base_selenium.LOGGER.info('Click Create New Test Unit')
        self.base_selenium.click(element='test_units:new_testunit')
        self.test_unit_page.sleep_tiny()
        # click on Overview, this will display an alert to the user
        self.base_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.base_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), 'https://automation.1lims.com/testUnits')
            self.base_selenium.LOGGER.info(' + clicking on Overview confirmed')
        else:
            self.base_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), 'https://automation.1lims.com/testUnits/add')
            self.base_selenium.LOGGER.info('clicking on Overview cancelled')

    def test025_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        """
        self.test_unit_page.get_random_test_units()
        test_units_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info('test_units_url: {}'.format(test_units_url))
        # click on Overview, it will redirect you to testunits' page
        self.base_selenium.LOGGER.info('click on Overview')
        self.base_page.click_overview()
        self.test_unit_page.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}testUnits'.format(self.base_selenium.url))
        self.base_selenium.LOGGER.info('clicking on Overview confirmed')

    @parameterized.expand(['Quantitative', 'Qualitative', 'MiBi'])
    def test_028_changing_testunit_type_update_fields_accordingly(self, testunit_type):
        """
        New: Test unit: Type Approach: When I change type from edit mode, the values should changed according to this type that selected 
        When I change type from edit mode, the values should changed according to this type that selected 
        LIMS-3680

        comment: this case will be handled in create
        """

        if testunit_type == 'MiBi':
            testunit_type = 'Quantitative MiBi'
            
        self.base_selenium.LOGGER.info('open testunits in create')
        self.test_unit_page.click_create_new_testunit()
        
        self.base_selenium.LOGGER.info('set the type to {}'.format(testunit_type))
        self.test_unit_page.set_testunit_type(testunit_type=testunit_type)
        self.test_unit_page.sleep_tiny()
        self.base_selenium.LOGGER.info('set testunit type to {}, fields should be displayed as the following'.format(testunit_type))
        
        if testunit_type == 'Quantitative':
            self.assertTrue(self.test_unit_page.check_for_quantitative_fields())
        elif testunit_type == 'Qualitative':
            self.assertTrue(self.test_unit_page.check_for_qualitative_fields())
        elif testunit_type == 'Quantitative MiBi':
            self.assertTrue(self.test_unit_page.check_for_quantitative_mibi_fields())

    
    def test_029_allow_user_to_change_between_specification_and_quantification(self):
        """
        New: Test unit: Edit mode:  Limit of quantification Approach: Allow user to change between the two options specification and limit of quantification from edit mode.
        Allow user to change between the two options specification and limit of quantification from edit mode.
        specification to quantifications
        """

        testunits_request = self.test_unit_api.get_all_test_units(filter='{"typeName":2}').json()
        self.assertEqual(testunits_request['status'], 1)
        testunits = testunits_request['testUnits']
        self.assertNotEqual(len(testunits), 0)
        testunit_name = ''
        for testunit in testunits:
            if testunit['specifications'] != '' and testunit['quantification'] == '':
                testunit_name = testunit['number']
                break
            
        if testunit_name == '':
            self.base_selenium.LOGGER.info('there is no testunit with specification only value')
            self.assertTrue(False)
        
        testunit_record = self.test_unit_page.search(value=testunit_name)[0]

        self.test_unit_page.open_edit_page(row=testunit_record)
        
        self.base_selenium.LOGGER.info('generate random lower/ upper limit')
        random_lower_limit = self.test_unit_page.generate_random_number(lower=0, upper=49)
        random_upper_limit = self.test_unit_page.generate_random_number(lower=50, upper=100)

        self.base_selenium.LOGGER.info('switch to quantification')
        self.test_unit_page.switch_from_spec_to_quan(lower_limit=random_lower_limit, upper_limit=random_upper_limit)
        self.base_selenium.LOGGER.info('refresh to make sure that data are updated successfully')
        self.base_selenium.refresh()

        self.assertEqual(self.test_unit_page.get_testunit_specification_type(), 'quan')
        self.assertEqual(self.test_unit_page.get_quan_upper_limit(), str(random_upper_limit))
        self.assertEqual(self.test_unit_page.get_quan_lower_limit(), str(random_lower_limit))
    
    
    def test_030_allow_user_to_change_between_specification_and_quantification(self):
        """
        New: Test unit: Edit mode:  Limit of quantification Approach: Allow user to change between the two options specification and limit of quantification from edit mode.
        Allow user to change between the two options specification and limit of quantification from edit mode.

        quantifications to specifications
        """

        testunits_request = self.test_unit_api.get_all_test_units(filter='{"typeName":2}').json()
        self.assertEqual(testunits_request['status'], 1)
        testunits = testunits_request['testUnits']
        self.assertNotEqual(len(testunits), 0)
        testunit_name = ''
        for testunit in testunits:
            if testunit['specifications'] == '' and testunit['quantification'] != '':
                testunit_name = testunit['name']
                break

        if testunit_name == '':
            self.base_selenium.LOGGER.info('there is no testunit with quantification only value')
            self.assertTrue(False)

        testunit_record = self.test_unit_page.search(value=testunit_name)[0]

        self.test_unit_page.open_edit_page(row=testunit_record)
        
        self.base_selenium.LOGGER.info('generate random lower/ upper limit')
        random_lower_limit = self.test_unit_page.generate_random_number(lower=0, upper=49)
        random_upper_limit = self.test_unit_page.generate_random_number(lower=50, upper=100)
        
        self.base_selenium.LOGGER.info('switch to specification')
        self.test_unit_page.switch_from_quan_to_spec(lower_limit=random_lower_limit, upper_limit=random_upper_limit)
        self.base_selenium.LOGGER.info('refresh to make sure that data are updated successfully')
        self.base_selenium.refresh()

        self.assertEqual(self.test_unit_page.get_testunit_specification_type(), 'spec')
        self.assertEqual(self.test_unit_page.get_spec_upper_limit(), str(random_upper_limit))
        self.assertEqual(self.test_unit_page.get_spec_lower_limit(), str(random_lower_limit))
    
    def test031_allow_unit_field_to_be_displayed_in_case_of_mibi(self):
        """
        New: Test unit: limit of quantification Approach: Allow the unit field to display when I select quantitative MiBi type & make sure it displayed in the active table & in the export sheet 
        
        Make sure the unit displayed in the active table & in the export sheet 
        In case I create test unit with type quantitative MiBi, Unit field opened beside the upper limit & the concentration. 

        LIMS-4162
        """

        testunit_record = self.test_unit_page.search(value='Quantitative MiBi')[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testunit_record)
        testunit_number = row_data['Test Unit No.']
        initial_unit = row_data['Unit']
        if initial_unit == '-':
            self.base_selenium.LOGGER.info('unit field has no value, update the record to make sure ')
            self.test_unit_page.open_edit_page(row=testunit_record)
            random_unit = self.test_unit_page.generate_random_text()
            self.test_unit_page.set_spec_unit(value=random_unit)
            self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save testunit')
            self.test_unit_page.get_test_units_page()

        testunit_record = self.test_unit_page.search(value=testunit_number)[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testunit_record)

        self.base_selenium.LOGGER.info('unit field has value {}'.format(row_data['Unit']))
        if initial_unit == '-':
            self.assertEqual(row_data['Unit'], random_unit)

        self.info(' * Download XSLX sheet')
        self.test_unit_page.download_xslx_sheet()
        rows_data = self.test_unit_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.base_selenium.LOGGER.info(' * Comparing the test units with index : {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.test_unit_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            self.base_selenium.LOGGER.info('search for value of the unit field: {}'.format(row_data['Unit']))
            self.assertIn(row_data['Unit'], fixed_sheet_row_data)

    def test032_editing_limit_of_quantification_fields_should_affect_table_and_version(self):
        """
        New: Test unit: Limits of quantification Approach: Versions:
        In case I edit any field in the limits of quantification and press on save and create new version,
        new version should create & display in the active table & versions table

        When I edit any field in limits of quantification and press on save and create new version ..new version created 
        This version should displayed in the active/archive table 
        This version should display in the versions table 

        LIMS-4423
        """
        testunits_request = self.test_unit_api.get_all_test_units(filter='{"typeName":2}').json()
        self.assertEqual(testunits_request['status'], 1)
        testunits = testunits_request['testUnits']
        self.assertNotEqual(len(testunits), 0)

        testunit_name = ''
        for testunit in testunits:
            if testunit['specifications'] == '':
                testunit_name = testunit['name']
                break

        self.base_selenium.LOGGER.info('generate random data to update testunit with')
        random_upper_limit = self.test_unit_page.generate_random_number(lower=50, upper=100)
        random_lower_limit = self.test_unit_page.generate_random_number(lower=0, upper=49)
        random_unit = self.test_unit_page.generate_random_text()

        testunit_record = self.test_unit_page.search(value=testunit_name)[0]
        testunit_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testunit_record)
        version_value = int(testunit_data['Version'])
        self.base_selenium.LOGGER.info('open the testunit in edi form to update it')
        self.test_unit_page.open_edit_page(row=testunit_record)

        self.base_selenium.LOGGER.info('set upper limit to {}'.format(random_upper_limit))
        self.test_unit_page.set_quan_upper_limit(value=random_upper_limit)

        self.base_selenium.LOGGER.info('set lower limit to {}'.format(random_lower_limit))
        self.test_unit_page.set_quan_lower_limit(value=random_lower_limit)

        self.base_selenium.LOGGER.info('set unit limit to {}'.format(random_unit))
        self.test_unit_page.set_quan_unit(value=random_unit)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save_and_create_new_version()

        self.base_selenium.LOGGER.info('refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()

        self.base_selenium.LOGGER.info(
            'upper limit is {}, and it should be {}'.format(self.test_unit_page.get_quan_upper_limit(),
                                                            str(random_upper_limit)))
        self.assertEqual(self.test_unit_page.get_quan_upper_limit(), str(random_upper_limit))

        self.base_selenium.LOGGER.info(
            'lower limit is {}, and it should be {}'.format(self.test_unit_page.get_quan_lower_limit(),
                                                            str(random_lower_limit)))
        self.assertEqual(self.test_unit_page.get_quan_lower_limit(), str(random_lower_limit))

        self.base_selenium.LOGGER.info(
            'unit is {}, and it should be {}'.format(self.test_unit_page.get_quan_unit(), str(random_unit)))
        self.assertEqual(self.test_unit_page.get_quan_unit(), str(random_unit))

        self.test_unit_page.get_test_units_page()

        testunit_record_after_update = self.test_unit_page.search(value=testunit_name)[0]
        testunit_data_after_update = self.base_selenium.get_row_cells_dict_related_to_header(
            row=testunit_record_after_update)

        self.base_selenium.LOGGER.info('making sure that version is updated successfully')
        self.base_selenium.LOGGER.info(
            'version is {}, ant it should be {}'.format(testunit_data_after_update['Version'], str(version_value + 1)))
        updated_version = str(version_value + 1)
        self.assertEqual(testunit_data_after_update['Version'], str(updated_version))
        self.assertEqual(testunit_data_after_update['Quantification Limit'],
                         str(random_lower_limit) + '-' + str(random_upper_limit))
        self.assertEqual(testunit_data_after_update['Quantification Limit Unit'], random_unit)

        self.test_unit_page.click_check_box(source=testunit_record_after_update)
        self.test_unit_page.get_versions_table()
        testunits_records_versions = self.test_unit_page.result_table()

        version_counter = 1
        record_counter = 0
        while record_counter < len(testunits_records_versions) - 1:
            record_data = self.base_selenium.get_row_cells_dict_related_to_header(
                row=testunits_records_versions[record_counter])
            self.assertEqual(record_data['Version'], str(version_counter))

            if version_counter == updated_version:
                self.assertEqual(record_data['Quantification Limit'],
                                 str(random_lower_limit) + '-' + str(random_upper_limit))
                self.assertEqual(record_data['Quantification Limit Unit'], random_unit)

            version_counter = version_counter + 1
            record_counter = record_counter + 1


    @skip('waiting for API deleting')
    def test033_archive_quantifications_limit_field(self):
        """
        New: Test unit: Configuration: Limit of quantification Approach: Display the new fields in the configuration section 
        ( Upper limit & lower limit & unit of  limit of quantification ) and I can archive them. 
        User can archive the quantification limits field from the configuration section 
        "Archive-allowed"
        LIMS-4164
        """
        self.test_unit_page.open_configurations()
        self.assertTrue(self.test_unit_page.archive_quantification_limit_field())
        self.assertFalse(
            self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
        self.test_unit_page.get_archived_fields_tab()
        self.assertTrue(self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.click_create_new_testunit()
        self.test_unit_page.set_testunit_type(testunit_type='Quantitative')
        self.assertFalse(self.base_selenium.check_element_is_exist(element='test_unit:use_quantification'))

    @skip('waiting for API deleting')
    def test034_restore_quantifications_limit_field(self):
        """
        New: Test unit: Configuration: Limit of quantification Approach: Display the new fields in the configuration section 
        ( Upper limit & lower limit & unit of  limit of quantification ) and I can archive them. 
        User can archive the quantification limits field from the configuration section 
        "Restore"
        LIMS-4164
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.get_archived_fields_tab()
        self.assertTrue(self.test_unit_page.restore_quantification_limit_field())
        self.assertFalse(
            self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
        self.test_unit_page.get_active_fields_tab()
        self.assertTrue(self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.click_create_new_testunit()
        self.test_unit_page.set_testunit_type(testunit_type='Quantitative')
        self.assertTrue(self.base_selenium.check_element_is_exist(element='test_unit:use_quantification'))

    def test035_test_unit_name_is_mandatory(self):
        """

        New: Test unit: Configuration: Test unit Name Approach: Make the test units field as as mandatory field (This mean you can't remove it )

        LIMS- 5651
        :return:
        """

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()

        self.assertTrue(self.test_unit_page.check_all_options_of_search_view_menu())

    @parameterized.expand(['name', 'method', 'type', 'number'])
    def test036_test_unit_name_allow_user_to_search_with_selected_options_testplan(self, search_view_option):
        """

        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with ( name, number, type, method ) in the drop down list of the analysis for

        LIMS- 6422
        :return:
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.select_option_to_view_search_with(view_search_options=[search_view_option])

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        material_type='All')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Search by the testunit name {} to get number'.format(new_random_name))
        row = self.test_unit_page.search(value=new_random_name)[0]
        new_auto_generated_number = self.base_selenium.get_row_cell_text_related_to_header(row=row,
                                                                                           column_value='Test Unit No.')

        new_auto_generated_number = new_auto_generated_number.replace("'", '')
        self.base_selenium.LOGGER.info('get the newly created testunit number of {}'.format(new_auto_generated_number))

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name='in progress')
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_name)
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=new_auto_generated_number)
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_method)

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = old_values.split('\n×')

        self.test_unit_page.select_option_to_view_search_with(view_search_options=old_values)

        if search_view_option == 'name':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'type':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option == 'number':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)

    def test037_test_unit_name_search_default_options_name_type_in_testplan(self):
        """

        New: Test unit: Configuration: Test units field Approach: Allow name & type to display by default in the test plan form In case I select them from the test unit configuration

        LIMS- 6423
        :return:
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.deselect_all_options_to_view_search_with()

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        material_type='All')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Search by the testunit name {} to get number'.format(new_random_name))
        row = self.test_unit_page.search(value=new_random_name)[0]
        new_auto_generated_number = self.base_selenium.get_row_cell_text_related_to_header(row=row,
                                                                                           column_value='Test Unit No.')

        new_auto_generated_number = new_auto_generated_number.replace("'", '')
        self.base_selenium.LOGGER.info('get the newly created testunit number of {}'.format(new_auto_generated_number))

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name='in progress')
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_name)
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=new_auto_generated_number)
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_method)

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = old_values.split('\n×')

        self.test_unit_page.select_option_to_view_search_with(view_search_options=old_values)

        self.assertTrue(is_name_exist)
        self.assertFalse(is_number_exist)
        self.assertTrue(is_type_exist)
        self.assertFalse(is_method_exist)

    def test038_test_unit_name_view_method_option_multiple_line_in_testplan(self):
        """

        New: Test Unit: Configuration: Test unit Name Approach: In case you select the method to display and you entered long text in it, the method should display into multiple lines (test plan )

        LIMS- 6424
        :return:
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string() + self.generate_random_string() + self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.select_option_to_view_search_with(view_search_options=['method'])

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        material_type='All')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name='in progress')
        is_method_exist = self.test_plan.set_test_unit(test_unit=new_random_method)
        multiple_lines_properties = self.test_plan.get_testunit_in_testplan_title_multiple_line_properties()

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = old_values.split('\n×')

        self.test_unit_page.select_option_to_view_search_with(view_search_options=old_values)

        self.assertEquals(multiple_lines_properties['textOverflow'],'clip')
        self.assertEquals(multiple_lines_properties['lineBreak'], 'auto')

    @parameterized.expand([('name', 'type'),
                           ('name', 'method'),
                           ('name', 'number'),
                           ('type', 'method'),
                           ('type', 'number'),
                           ('method', 'number')
                           ])
    def test039_test_unit_name_allow_user_to_search_with_selected_two_options_testplan(self, search_view_option1,
                                                                                       search_view_option2):
        """

        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with ( name, number, type, method ) in the drop down list of the analysis for

        LIMS- 6426
        :return:
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.select_option_to_view_search_with(view_search_options=[search_view_option1,search_view_option2])

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Create new testunit with qualitative and random generated data')
        self.test_unit_page.create_qualitative_testunit(name=new_random_name, method=new_random_method,
                                                        material_type='All')
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Search by the testunit name {} to get number'.format(new_random_name))
        row = self.test_unit_page.search(value=new_random_name)[0]
        new_auto_generated_number = self.base_selenium.get_row_cell_text_related_to_header(row=row,
                                                                                           column_value='Test Unit No.')
        new_auto_generated_number = new_auto_generated_number.replace("'", '')
        self.base_selenium.LOGGER.info('get the newly created testunit number of {}'.format(new_auto_generated_number))

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name='in progress')
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_name)
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=new_auto_generated_number)
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=new_random_method)

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = old_values.split('\n×')

        self.test_unit_page.select_option_to_view_search_with(view_search_options=old_values)

        if search_view_option1 == 'name' and search_view_option2 == 'type':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'name' and search_view_option2 == 'method':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'name' and search_view_option2 == 'number':
            self.assertTrue(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'type' and search_view_option2 == 'method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'type' and search_view_option2 == 'number':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'method' and search_view_option2 == 'number':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)

    def test040_testunits_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page
        LIMS-6201
        """
        testunits = self.get_all_test_units()
        testunit_name = random.choice(testunits)['name']
        search_results = self.test_unit_page.search(testunit_name)
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Test Unit Name'] == testunit_name:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(testunit_name, search_data['Test Unit Name'])
        # Navigate to articles page
        self.info('navigate to articles page')
        self.articles_page.get_articles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}articles'.format(self.base_selenium.url))

    def test041_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        assert (self.test_unit_page.deselect_all_configurations(), False)
