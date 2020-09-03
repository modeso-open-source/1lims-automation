from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.articles_page import Articles
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.testunits_page import TstUnits
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from ui_testing.pages.order_page import Order
from ui_testing.pages.login_page import Login
from api_testing.apis.users_api import UsersAPI
from unittest import skip
from parameterized import parameterized
from nose.plugins.attrib import attr
import re, random


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.test_unit_page = TstUnit()
        self.test_units_page = TstUnits()
        self.test_plan = TstPlan()
        self.article_api = ArticleAPI()
        self.test_unit_api = TestUnitAPI()
        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_configuration()
        self.test_unit_page.get_test_units_page()

    #@skip('https://modeso.atlassian.net/browse/LIMS-5237')
    @skip('https://modeso.atlassian.net/browse/LIMSA-207')
    def test001_test_units_search(self):
        """
        New: Test units: Search Approach: I can search by any field in the table view

        LIMS-3674
        """
        row = self.test_unit_page.get_random_test_units_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) \
                    or row_data[column] == '-' or not (row_data[column]) or row_data[column] == 'N/A':
                continue
            self.info('search for {} : {}'.format(column, row_data[column]))
            if column == 'Unit':
                unit_format = self.test_unit_api.get_unit_format(row_data['Test Unit No.'])
                search_results = self.test_unit_page.search(unit_format)
            else:
                search_results = self.test_unit_page.search(
                    row_data[column].replace('-', '_').replace("<= ", '').replace(">= ", ''))
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    @skip('https://modeso.atlassian.net/browse/LIMSA-207')
    def test002_archive_test_units(self):
        """
        New: Test units: Archive Approach: I can archive any test unit successfully.

        LIMS-3670
        """
        self.info('select random multiple rows')
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        self.info('Archive selected test units')
        self.test_unit_page.archive_selected_test_units()
        self.info('Navigate to archived test unit table')
        self.test_unit_page.get_archived_test_units()
        for test_unit in selected_test_units_data:
            self.info(' + {} Test Unit should be activated.'.format(test_unit['Test Unit No.']))
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit['Test Unit No.']))

    @skip('https://modeso.atlassian.net/browse/LIMSA-207')
    def test003_restore_test_units(self):
        """
        New: Test units: Restore Approach: I can restore any test unit successfully.

        LIMS-5262
        """
        selected_test_unit = []
        self.info('Navigate to archived test unit table')
        self.test_unit_page.get_archived_test_units()
        self.info('select random multiple rows')
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        for test_unit in selected_test_units_data:
            selected_test_unit.append(test_unit['Test Unit No.'])
        self.info('Restore selected test units')
        self.test_unit_page.restore_selected_test_units()
        self.info('Navigate to active test unit table')
        self.test_unit_page.get_active_test_units()
        for test_unit in selected_test_unit:
            self.info(' + {} Test Unit is restored'.format(test_unit))
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit))

    def test004_check_version_after_update(self):
        """
        Test unit: Version Approach: After I update any field then press on save and
        create new version , new version created in the active table.

        LIMS-3676

        New: Test units: Edit Approach: User can edit in (test unit name & test unit number
        & category & method & iteration & materiel type and the specification )

        LIMS-5288
        """
        self.info("select random test unit")
        random_test_unit = random.choice(self.test_unit_api.get_all_testunits_json())
        self.assertTrue(random_test_unit, "No test unit selected")
        update_data = self.test_unit_page.update_test_unit(random_test_unit['id'])
        self.info('Refresh to make sure that the new data are saved')
        test_unit_after_update = self.test_unit_page.refresh_and_get_updated_data()
        self.assertEqual(update_data, test_unit_after_update)
        self.test_units_page.get_test_units_page()
        first_testunit_data = self.test_units_page.filter_and_get_result(text=test_unit_after_update['number'])
        self.info('+ Assert testunit version is: {}, new version: {}'.
                  format(random_test_unit['version'], first_testunit_data['Version']))
        self.assertEqual(str(random_test_unit['version']+1), first_testunit_data['Version'])

    def test005_quantative_mibi_not_entering_dash_in_upper_limit(self):
        """
        Upper limit Approach, user can't enter  in the upper limit

        LIMS-3768
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        self.info('Create new test unit with Quantitative MiBi and random generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type='Quantitative MiBi',
                                                method=new_random_method, upper_limit='-')

        self.test_unit_page.save()
        self.info('Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('+ Assert error msg which indicates that it does not allow to add - in upper limit has appeared? {}'.
                  format(validation_result))
        self.assertEqual(validation_result, True)

    def test006_search_by_archived_testunit(self):
        """
        Archived test units shouldn't display in the test plan step two & also in the analysis step two.

        LIMS-3677
        """
        self.info("get random archived test unit data")
        response, payload = self.test_unit_api.get_all_test_units(deleted="1")
        self.assertEqual(response['status'], 1, payload)
        archived_test_unit = random.choice(response['testUnits'])
        self.info("archived test unit data {}".format(archived_test_unit))
        self.info('get random In Progrees test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.base_selenium.click('test_plan:next')
        self.base_selenium.click('test_plan:add_new_item')
        self.info('Assert that archived test unit is not existing')
        self.assertFalse(self.base_selenium.is_item_in_drop_down(
            element='test_plan:test_unit', item_text=archived_test_unit['name']))

    @parameterized.expand(['spec', 'quan'])
    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test007_allow_unit_field_to_be_optional(self, specification_type):
        """
        Test unit: Limit of quantification Approach: Allow unit field to be optional field
        in case I select specification or limit of quantification.

        LIMS-4161
        """
        self.info('create Quantitative test unit using api')
        if specification_type == 'spec':
            response, payload = self.test_unit_api.create_quantitative_testunit()
        else:
            upperLimit = self.generate_random_number(lower=50, upper=100)
            lowerLimit = self.generate_random_number(lower=1, upper=49)
            response, payload = self.test_unit_api.create_quantitative_testunit(useSpec=False, useQuantification=True,
                                                                                quantificationUpperLimit=upperLimit,
                                                                                quantificationLowerLimit=lowerLimit)

        self.assertEqual(response['status'], 1, 'test unit not created with payload {} '.format(payload))
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(payload['number']))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(payload['number'])
        self.info('Checking with upper and lower limit to make sure that data saved normally')
        if specification_type == 'spec':
            self.assertEqual(str(payload['lowerLimit'])+'-'+str(payload['upperLimit']),
                             test_unit_found['Specifications'])
            self.info('+ Assert unit value after save is: {}, and should be empty'.format(test_unit_found['Unit']))
            self.assertEqual(test_unit_found['Unit'], '-')
        else:
            self.assertEqual(str(payload['quantificationLowerLimit'])+'-'+str(payload['quantificationUpperLimit']),
                             test_unit_found['Quantification Limit'])
            self.info('+ Assert unit value after save is: {}, and should be empty'.format(
                test_unit_found['Quantification Limit Unit']))
            self.assertEqual(test_unit_found['Quantification Limit Unit'], '-')

    @parameterized.expand(['spec', 'quan'])
    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test008_force_use_to_choose_specification_or_limit_of_quantification(self, specification_type):
        """
        The specification & Limit of quantification one of them should be mandatory.

        LIMS-4158
        """
        self.info('Prepare random data for the new test unit')
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)
        self.info('Create new test unit with the randomly generated data')
        test_unit_no = self.test_unit_page.create_new_testunit(name=new_random_name,
                                                               testunit_type='Quantitative',
                                                               method=new_random_method)
        self.info('Create new test unit with the random data')
        self.test_unit_page.save(sleep=False)
        self.info('Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Checking that a validation message actually appeared which means that user can not'
                  'create test unit without choosing specification of limit of quantification')
        self.assertEqual(validation_result, True)
        self.test_unit_page.sleep_tiny()
        self.info('Set the testunit to be: {}'.format(specification_type))
        self.test_unit_page.use_specification_or_quantification(type_to_use=specification_type)
        if specification_type == 'spec':
            self.test_unit_page.set_spec_upper_limit(value=new_random_upper_limit)
        elif specification_type == 'quan':
            self.test_unit_page.set_quan_upper_limit(value=new_random_upper_limit)

        self.test_unit_page.save_and_wait()
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(test_unit_no))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(test_unit_no)
        self.assertTrue(test_unit_found)
        self.info('Checking with upper limit to make sure that data saved normally')
        if specification_type == 'spec':
            self.assertEqual('<= ' + str(new_random_upper_limit), test_unit_found['Specifications'])
        else:
            self.assertEqual('<= ' + str(new_random_upper_limit), test_unit_found['Quantification Limit'])

    @parameterized.expand(['Qualitative', 'Quantitative MiBi'])
    def test009_qualitative_value_should_be_mandatory_field(self, testunit_type):
        """
        The qualitative value should be mandatory field in the qualitative type

        LIMS-3766
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        self.info('Create new test unit with Quantitative MiBi and random generated data')
        self.test_unit_page.create_new_testunit(name=new_random_name, testunit_type=testunit_type,
                                                method=new_random_method)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit')

        self.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.info('Assert error msg')
        self.assertEqual(validation_result, True)

    @skip('https://modeso.atlassian.net/browse/LIMS-8467')
    def test010_material_type_approach(self):
        """"
        In case I created test unit with 4 materiel type, when I go to test plan,
        I should found that each test unit displayed according to it's materiel type.

        LIMS-3683
        """
        self.info('create new test unit with 4 material type')
        testunit = self.test_unit_api.create_test_unit_with_multiple_material_types()
        self.info('created test unit data {}'.format(testunit))
        self.info('Navigate to test plan page')
        self.test_plan.get_test_plans_page()
        self.info('create new test plan')
        self.test_plan.create_new_test_plan(material_type=testunit['selectedMaterialTypes'][0]['name'],
                                            test_unit=testunit['name'], save=False)

        test_unit_data = self.test_plan.get_all_testunits_in_testplan(navigate_to_test_unit_selection=False)
        self.assertIn(testunit['name'], test_unit_data[0][0])

        for i in range(0, len(testunit['selectedMaterialTypes'])-1):
            if i+1 < len(testunit['selectedMaterialTypes']):
                self.base_selenium.click('test_plan:back_button')
                self.test_plan.clear_material_types()
                self.test_plan.set_material_type(testunit['selectedMaterialTypes'][i+1]['name'])
                self.test_plan.set_article(random=True)
            else:
                break

            self.assertCountEqual(test_unit_data, self.test_plan.get_all_testunits_in_testplan())
        self.info("test unit displayed according to materiel type.")

    @parameterized.expand(['True', 'False'])
    def test011_create_test_unit_with_random_category(self, select_from_drop_down):
        """
        Test unit: Category Approach: I can select from the drop down list or create new category

        LIMS-3682
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        if select_from_drop_down == 'False':
            new_random_category = self.generate_random_string()
            self.info("Create new test unit with category {}".format(new_random_category))
        else:
            self.info("Create new test unit with random category")
            new_random_category = ''
        test_unit_no = self.test_unit_page.create_qualitative_testunit(name=new_random_name,
                                                                       method=new_random_method,
                                                                       category=new_random_category)
        self.test_unit_page.save_and_wait()
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(test_unit_no))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(test_unit_no)
        self.assertTrue(test_unit_found)
        self.info('Assert category : {}'.format(test_unit_found['Category']))
        if random == 'True':
            self.assertEqual(new_random_category, test_unit_found['Category'])
        else:
            self.assertTrue(test_unit_found['Category'])

    @parameterized.expand([('upper', 'spec'),
                           ('upper', 'quan'),
                           ('lower', 'spec'),
                           ('lower', 'quan')
                           ])
    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test012_create_test_unit_with_one_limit_only(self, limit, spec_or_quan):
        """
        New: Test unit: Specification Approach: In case I entered the upper limit or the lower limit only,
        the specification should display <=or >= according to that in the table view.

        LIMS-3681
        LIMS-4415
        """
        self.info('Create new test unit with qualitative and random generated data')
        if limit == "upper":
            self.info('Create with upper limit')
            if spec_or_quan == 'spec':
                response, payload = self.test_unit_api.create_quantitative_testunit(lowerLimit='')
            else:
                upperLimit = self.generate_random_number(lower=50, upper=100)
                response, payload = self.test_unit_api.create_quantitative_testunit(useSpec=False,
                                                                                    useQuantification=True,
                                                                                    quantificationUpperLimit=upperLimit,
                                                                                    quantificationLowerLimit='')

        else:
            self.info('Create with lower limit')
            if spec_or_quan == 'spec':
                response, payload = self.test_unit_api.create_quantitative_testunit(upperLimit='')
            else:
                lowerLimit = self.generate_random_number(lower=1, upper=49)
                response, payload = self.test_unit_api.create_quantitative_testunit(useSpec=False,
                                                                                    useQuantification=True,
                                                                                    quantificationUpperLimit='',
                                                                                    quantificationLowerLimit=lowerLimit)
        self.assertEqual(response['status'], 1, payload)
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(payload['number']))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(payload['number'])
        if limit == "upper":
            self.info('Check that <= is existing in {}'.format(spec_or_quan))
            self.assertIn('<=', test_unit_found['Specifications']) if 'spec' in spec_or_quan \
                else self.assertIn('<=', test_unit_found['Quantification Limit'])
        else:
            self.info('Check that >= is existing in specifications')
            self.assertIn('>=', test_unit_found['Specifications']) if 'spec' in spec_or_quan \
                else self.assertIn('>=', test_unit_found['Quantification Limit'])

    def test013_create_quantitative_mibi_test_unit(self):
        """
        New: Test units: Creation Approach: User can create test unit with quantitative
        MiBi type successfully.

        LIMS-5287
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_limit = self.generate_random_number(lower=500, upper=1000)
        self.info('Create new Quantitative MiBi test unit')
        self.info('Create with upper limit : {}'.format(new_random_limit))
        test_unit_no = self.test_unit_page.create_quantitative_mibi_testunit(
            name=new_random_name, method=new_random_method, upper_limit=new_random_limit)

        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save_and_wait()
        self.info('Get the test unit of it')
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(test_unit_no)
        self.assertEqual(test_unit_found['Test Unit Name'], new_random_name)

    def test014_quantitative_mibi_type_not_allow_upper_limit_the_concentration_to_be_mandatory_fields(self):
        """
        All specifications fields should not be mandatory in the edit mode

        LIMS-3769
        """
        self.info('Create new Quantitative MiBi test unit')
        response, payload = self.test_unit_api.create_mibi_testunit()
        self.assertEqual(response['status'], 1, " test unit not created with payload {}".format(payload))
        self.test_unit_page.open_test_unit_edit_page_by_id(response['testUnit']['testUnitId'])
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.clear_spec_upper_limit()
        self.test_unit_page.clear_cons()
        self.test_unit_page.save(save_btn='general:save_form', logger_msg='Save new testunit, should fail')
        self.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert error msg')
        self.assertEqual(validation_result, True)

    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test015_specification_limit_of_quantification_approach(self):
        """
        New: Test unit: Specification/limit of quantification Approach: Allow user to select those both options
        ( specification & limit of quantification ) at the same time ( create test unit with both selection )

        LIMS-4159
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        new_random_upper_limit = self.generate_random_number(lower=500, upper=1000)
        new_random_lower_limit = self.generate_random_number(lower=1, upper=500)
        spec_or_quan = 'spec_quan'
        self.info('Create new testunit with qualitative and random generated data')
        test_unit_no = self.test_unit_page.create_quantitative_testunit(
            name=new_random_name, method=new_random_method, upper_limit=new_random_upper_limit,
            lower_limit=new_random_lower_limit, spec_or_quan=spec_or_quan)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save_and_wait()
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(test_unit_no))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(test_unit_no)
        self.info('Assert upper and lower limits are in specifications')
        self.assertEqual("{}-{}".format(new_random_lower_limit, new_random_upper_limit),
                         test_unit_found['Specifications'])

        self.info('Assert upper and lower limits are in quantification_limit')
        self.assertEqual("{}-{}".format(new_random_lower_limit, new_random_upper_limit),
                         test_unit_found['Quantification Limit'])

    def test016_fields_of_the_specification_limits_of_quant_should_be_disabled_if_the_checkbox_is_not_selected(self):
        """
        The fields of the specification & limits of quantification should be disabled if the checkbox is not selected

        LIMS-4418
        """
        new_random_name = self.generate_random_string()
        new_random_method = self.generate_random_string()
        self.info('Create new Qualitative testunit with random generated data')
        self.test_unit_page.create_quantitative_testunit(name=new_random_name,
                                                         method=new_random_method, spec_or_quan="")
        self.info('Assert that all limits fields are not active')
        for limit in ['quan_upper', 'quan_lower', 'spec_upper', 'spec_lower']:
            class_attr = self.base_selenium.get_attribute('test_unit:{}_limit'.format(limit), 'class')
            self.info('Assert that {}_limit is not active'.format(limit))
            self.assertNotIn('ng-valid', class_attr)

    @parameterized.expand(['quan', 'spec'])
    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test017_create_quantative_with_limits_of_quantative_only_and_specification_only(self, limits_type):
        """
        New:Test unit: Create Approach: User can create test unit with limits of quantification type only &
        with upper lower limits
        New: Test unit: Creation Approach: User can create test units with Quantitative type with specification only

        LIMS-5427
        LIMS-4156

        New: Test units : Limits of quantification Approach: In case I didn't enter empty values in the upper/lower
        limits of the specification of limits of quantification, it should display N/A in the active table

        LIMS-4427
        """
        new_name = self.generate_random_string()
        new_method = self.generate_random_string()
        new_random_limit = self.generate_random_number()
        test_unit_no = self.test_unit_page.create_quantitative_testunit(
            name=new_name, upper_limit=new_random_limit, lower_limit=new_random_limit,
            spec_or_quan=limits_type, method=new_method)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save_and_wait()
        self.info('Get the test unit of it')
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(test_unit_no))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(test_unit_no)
        self.assertTrue(test_unit_found)
        if limits_type == 'quan':
            self.assertNotEqual(test_unit_found['Quantification Limit'], 'N/A')
            self.assertEqual(test_unit_found['Specifications'], 'N/A')
        else:
            self.assertNotEqual(test_unit_found['Specifications'], 'N/A')
            self.assertEqual(test_unit_found['Quantification Limit'], 'N/A')

    @skip('https://modeso.atlassian.net/browse/LIMSA-222')
    def test018_download_test_units_sheet(self):
        """
        I can download all the data in the table view in the excel sheet

        LIMS-3672-case of all data
        """
        self.info('download XSLX sheet')
        self.test_unit_page.download_xslx_sheet()
        rows_data = list(filter(None, self.test_unit_page.get_table_rows_data()))
        for index in range(len(rows_data)):
            self.info('comparing the test units with index : {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.test_unit_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            self.info(fixed_sheet_row_data)
            for item in fixed_row_data:
                if item == 'N/A' or str(item)[-3:] == '...':
                    continue
                self.assertIn(item, fixed_sheet_row_data)

    def test019_specification_limit_of_quantification_approach_can_be_minus(self):
        """
        New: Test unit: Quantitative: Specification Approach User can enter (-) in upper/lower limit

        LIMS-3767
        """
        self.info('Create new Qualitative test unit with - in upper and lower limit')
        response, payload = self.test_unit_api.create_quantitative_testunit(upperLimit='-', lowerLimit='-')
        self.assertEqual(response['status'], 1, payload)
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(payload['number']))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(payload['number'])
        self.info('Assert test unit created successfully')
        self.assertTrue(test_unit_found)
        self.info('Assert upper and lower limits are in specifications with N/A values')
        self.assertEqual("N/A", test_unit_found['Specifications'])

    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test020_change_quantification_limits_not_effect_test_plan(self):
        """
        New: Test units/effect on test plan: Limits of quantification Approach: In case I
        make any edit in the limits of quantification, this shouldn't effect on test plan

        LIMS-4420
        """
        self.info("Create new quantitative testunit with quantification limits")
        oldUpperLimit = self.generate_random_number(lower=50, upper=100)
        oldLowerLimit = self.generate_random_number(lower=1, upper=49)
        tu_response, tu_payload = self.test_unit_api.create_quantitative_testunit(
            quantificationUpperLimit=oldUpperLimit, quantificationLowerLimit=oldLowerLimit,
            useQuantification=True, useSpec=False)
        self.assertEqual(tu_response['status'], 1, tu_payload)
        testunit_display_old_quantification_limit = '{}-{}'.format(
            tu_payload['quantificationLowerLimit'], tu_payload['quantificationUpperLimit'])

        test_plan = TestPlanAPI().create_testplan_from_test_unit_id(tu_response['testUnit']['testUnitId'])
        self.assertTrue(test_plan, "failed to create test plan")
        self.info('change upper limits of the test unit')
        self.test_unit_page.open_test_unit_edit_page_by_id(tu_response['testUnit']['testUnitId'])
        self.test_unit_page.sleep_small()
        self.test_unit_page.set_quan_upper_limit('1000')
        self.test_unit_page.set_quan_lower_limit('100')
        self.test_unit_page.save_and_wait()
        self.test_plan.get_test_plans_page()
        self.test_plan.filter_by_testplan_number(test_plan['number'])
        child_table_data = self.test_plan.get_child_table_data()[0]
        self.info('assert that limits have not changed')
        self.assertEqual(child_table_data['Quantification Limit'], testunit_display_old_quantification_limit)

    def test021_create_multi_test_units_with_same_name(self):
        """
        New: Test unit: Creation Approach; In case I create two test units with the same name,
        when I go to the test plan I found both of those with the same name

        LIMS-3684
        """
        test_unit_name = self.generate_random_string()
        self.info("create three test unit of diff. types, 'all' material and same name {}".format(test_unit_name))
        first_response, first_test_unit = self.test_unit_api.create_qualitative_testunit(name=test_unit_name)
        self.assertEqual(first_response['status'], 1, 'test unit not created {}'.format(first_test_unit))
        second_response, second_test_unit = self.test_unit_api.create_mibi_testunit(name=test_unit_name)
        self.assertEqual(second_response['status'], 1, 'test unit not created {}'.format(first_test_unit))
        third_response, third_test_unit = self.test_unit_api.create_quantitative_testunit(name=test_unit_name)
        self.assertEqual(third_response['status'], 1, 'test unit not created {}'.format(first_test_unit))
        self.test_plan.get_test_plans_page()
        self.info('create new test plan')
        self.test_plan.create_new_test_plan(save=False)
        self.base_selenium.click('test_plan:next')
        self.test_plan.sleep_tiny()
        self.base_selenium.click('test_plan:add_new_item')
        self.test_plan.sleep_tiny()
        self.info('get test unit suggestion list')
        test_units = self.base_selenium.get_drop_down_suggestion_list(element='test_plan:test_unit',
                                                                      item_text=test_unit_name)
        self.info('assert that 3 test units are in the suggestions list')
        self.test_plan.sleep_tiny()
        self.assertEqual(len(test_units), 3, test_units)

    def test022_duplicate_test_unit(self):
        """"
        New: Test unit: Duplication Approach: I can duplicate the test unit with only one record

        LIMS-3678- case 1
        """
        duplicated_test_unit_number = str(self.test_unit_api.get_auto_generated_testunit_no()[0]['id'])
        self.info('The duplicated test unit should have the number: {}'.format(duplicated_test_unit_number))
        self.info('Choosing a random test unit table row')
        random_test_unit = self.test_unit_page.select_random_table_row()
        test_unit_name = random_test_unit['Test Unit Name']
        self.info('test unit name : {}'.format(test_unit_name))
        self.test_unit_page.duplicate_test_unit()
        self.test_unit_page.sleep_small()
        found_testunit_data = self.test_units_page.filter_and_get_result(text=duplicated_test_unit_number)
        data_changed = ['Test Unit No.', 'Changed On', 'Created On', 'Version']
        random_test_unit_list, found_testunit_data_list = self.remove_unduplicated_data(
            data_changed=data_changed, first_element=random_test_unit, second_element=found_testunit_data)
        self.info('Asserting that the data is duplicated correctly')
        self.assertEqual(random_test_unit_list, found_testunit_data_list)

    def test023_duplicate_multiple_test_units(self):
        """"
        New: Test unit: Duplication Approach: I can't duplicate multiple test units

        LIMS-3678- case 2
        """
        self.info('Choosing a random test unit table rows')
        self.test_unit_page.select_random_multiple_table_rows()
        self.info('duplicate the selected test units')
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click('orders:duplicate')
        error_msg = self.base_selenium.get_text(element='general:cant_delete_message')
        self.assertIn('Can not duplicate more than one record at once', error_msg)

    @parameterized.expand([('unitsub', 'qualitative'),
                           ('unitsub', 'quantitative'),
                           ('unitsuper', 'qualitative'),
                           ('unitsuper', 'quantitative'),
                           ('unitsub', 'quantitative MiBi'),
                           ('unitsuper', 'quantitative MiBi')
                           ])
    def test024_test_unit_with_sub_and_super_scripts_appears_in_exported_sheet(self, unit_with_sub_or_super, type):
        """
        New: Test unit: Export: Sub & Super scripts Approach: Allow user to see the
        sub & super scripts in the export file

        LIMS-5795

        Test unit : Unit: Subscript and superscript scripts Approach: Allow the unit
        filed to accept sub and super scripts in the test unit form

        LIMS-5784

        Test unit form: Unit accepts subscript and superscript characters in case of
        quantitative type with limit of quantification unit

        LIMS-5785

        Test unit: Export: Sub & Super scripts Approach:  Allow user to see the sub &
        super scripts in the export file

        LIMS-5810

        Test unit: Export: Sub & Super scripts Approach: Allow user to see the sub
         & super scripts in the export file ( quantitative MiBi )
        """
        
        if unit_with_sub_or_super == 'unitsub' and type == 'qualitative':
            response, payload = self.test_unit_api.create_qualitative_testunit(unit='[sub]')
            preview_unit = 'sub'
        elif unit_with_sub_or_super == 'unitsuper' and type == 'qualitative':
            response, payload = self.test_unit_api.create_qualitative_testunit(unit='{super}')
            preview_unit = 'super'
        elif unit_with_sub_or_super == 'unitsub' and type == 'quantitative':
            response, payload = self.test_unit_api.create_quantitative_testunit(unit='[sub]')
            preview_unit = 'sub'
        elif unit_with_sub_or_super == 'unitsuper' and type == 'quantitative':
            response, payload = self.test_unit_api.create_quantitative_testunit(unit='{super}')
            preview_unit = 'super'
        elif unit_with_sub_or_super == 'unitsub' and type == 'quantitative MiBi ':
            response, payload = self.test_unit_api.create_mibi_testunit(unit='[sub]')
            preview_unit = 'sub'
        else :
            response, payload = self.test_unit_api.create_mibi_testunit(unit='{super}')
            preview_unit = 'super'


        self.assertEqual(response['status'], 1, 'test unit not createed {}'.format(payload))
        self.test_unit_page.apply_filter_scenario(
            filter_element='test_units:testunit_number_filter',
            filter_text=payload['number'], field_type='text')
        self.test_unit_page.download_xslx_sheet()
        rows_data = self.test_unit_page.get_table_rows_data()
        self.info('Comparing the unit name in test unit table')
        fixed_row_data = self.fix_data_format(rows_data[0].split('\n'))
        self.assertIn(preview_unit, fixed_row_data)
        self.info('Comparing the unit name in xsxl sheet')
        values = self.test_unit_page.sheet.iloc[0].values
        fixed_sheet_row_data = self.fix_data_format(values)
        self.assertIn(preview_unit, fixed_sheet_row_data)

    @parameterized.expand(['quantitative', 'qualitative'])
    def test025_create_test_unit_appears_in_version_table(self, unit_type):
        """
        New: Test unit: Versions Approach: After you create new record,
        all the columns should display in the version table

        LIMS-5289
        """
        if unit_type == 'quantitative':
            self.info('Create new Quantitative testunit')
            response, payload = self.test_unit_api.create_quantitative_testunit()
        else:
            self.info('Create new Qualitative testunit')
            response, payload = self.test_unit_api.create_qualitative_testunit()

        self.assertEqual(response['status'], 1, 'test unit not created {}'.format(payload))
        test_unit_data, version_data = self.test_units_page.filter_and_get_version(payload['number'])

        for key, value in version_data[0].items():
            if key in test_unit_data.keys():
                if key == 'Test Unit No.':
                    self.assertEqual(value, test_unit_data['Test Unit No.'] + '.1')
                else:
                    self.assertEqual(value, test_unit_data[key], key)

    @parameterized.expand(['ok', 'cancel'])
    def test026_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.info('Click Create New Test Unit')
        self.base_selenium.click(element='test_units:new_testunit')
        self.test_unit_page.sleep_medium()
        self.info("click on Overview, this will display an alert to the user")
        self.test_unit_page.click_overview()
        if 'ok' == ok:
            self.test_unit_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testUnits'.format(self.base_selenium.url))
            self.info(' + clicking on Overview confirmed')
        else:
            self.test_unit_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testUnits/add'.format(self.base_selenium.url))
            self.info('clicking on Overview cancelled')

    @parameterized.expand(['No-edits', 'With_edits'])
    def test027_edit_approach_overview_button(self, edit):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202/LIMS-6818

        -Popup should appear when editing then clicking on overview without saving <All data will be lost>
        LIMS-6812
        """
        self.info('open edit page of random test unit')
        random_test_unit = random.choice(self.test_unit_api.get_all_testunits_json())
        self.test_unit_page.open_test_unit_edit_page_by_id(random_test_unit['id'])
        test_units_url = self.base_selenium.get_url()
        self.info('test_units_url: {}'.format(test_units_url))
        self.info("click on Overview, it will redirect you to testunits' page")
        if edit == 'No-edits':
            self.test_unit_page.click_overview()
            self.test_unit_page.sleep_tiny()
            self.info('Clicked overview without editing - Asserting active table is displayed')
            self.assertEqual(self.base_selenium.get_url(), '{}testUnits'.format(self.base_selenium.url))
            self.info('clicking on Overview confirmed')
        else:
            self.test_unit_page.update_test_unit(id=random_test_unit['id'], save=False)
            self.test_unit_page.click_overview()
            self.info('Clicked overview after editing without saving - Asserting popup appears')
            self.assertTrue(self.test_unit_page.confirm_popup(check_only=True))

    @parameterized.expand(['Quantitative', 'Qualitative', 'Quantitative MiBi'])
    def test028_changing_testunit_type_update_fields_accordingly(self, testunit_type):
        """
        New: Test unit: Type Approach: When I change type from edit mode, the values should
        changed according to this type that selected

        comment: this case will be handled in create

        LIMS-3680
        """
        self.info('click on create new test unit')
        self.test_unit_page.click_create_new_testunit()
        self.test_unit_page.sleep_medium()
        self.info('set the type to {}'.format(testunit_type))
        self.test_unit_page.set_testunit_type(testunit_type=testunit_type)
        self.test_unit_page.sleep_tiny()
        self.info(' assert that fields displayed as selected type')
        if testunit_type == 'Quantitative':
            self.assertTrue(self.test_unit_page.check_for_quantitative_fields())
        elif testunit_type == 'Qualitative':
            self.assertTrue(self.test_unit_page.check_for_qualitative_fields())
        elif testunit_type == 'Quantitative MiBi':
            self.assertTrue(self.test_unit_page.check_for_quantitative_mibi_fields())

    def test029_allow_user_to_change_from_specification_to_quantification(self):
        """
        New: Test unit: Edit mode:  Limit of quantification Approach: Allow user to change between
        the two options specification and limit of quantification from edit mode.

        LIMS-4160
        """
        self.info('select random quantitative unit with specification only ')
        test_unit_id = self.test_unit_api.get_test_unit_with_spec_or_quan_only('spec')
        self.assertTrue(test_unit_id, "No test unit selected")
        self.test_unit_page.open_test_unit_edit_page_by_id(id=test_unit_id)
        self.info('switch to quantification')
        self.test_unit_page.switch_from_spec_to_quan(lower_limit=50, upper_limit=100)
        self.info('refresh to make sure that data are updated successfully')
        self.base_selenium.refresh()
        self.assertEqual(self.test_unit_page.get_testunit_specification_type(), 'quan')
        self.assertEqual(self.test_unit_page.get_quan_upper_limit(), '100')
        self.assertEqual(self.test_unit_page.get_quan_lower_limit(), '50')

    def test030_allow_user_to_change_to_specification_from_quantification(self):
        """
        New: Test unit: Edit mode:  Limit of quantification Approach: Allow user to change between
        the two options specification and limit of quantification from edit mode.

        LIMS-4160
        """
        self.info('select random quantitative unit with quantification only ')
        res, payload = self.test_unit_api.create_quantitative_testunit(useSpec=False,
                                                                       useQuantification=True,
                                                                       quantificationUpperLimit=100,
                                                                       quantificationLowerLimit=10)
        self.assertEqual(res['message'], 'operation_success')
        test_unit_id = res['testUnit']['testUnitId']
        self.test_unit_page.open_test_unit_edit_page_by_id(id=test_unit_id)
        self.info('switch to specification')
        self.test_unit_page.switch_from_quan_to_spec(lower_limit=50, upper_limit=100)
        self.info('refresh to make sure that data are updated successfully')
        self.base_selenium.refresh()
        self.assertEqual(self.test_unit_page.get_testunit_specification_type(), 'spec')
        self.assertEqual(self.test_unit_page.get_spec_upper_limit(), '100')
        self.assertEqual(self.test_unit_page.get_spec_lower_limit(), '50')

    def test031_allow_unit_field_to_be_displayed_in_case_of_mibi(self):
        """
        New: Test unit: limit of quantification Approach: Allow the unit field to display
        when I select quantitative MiBi type & make sure it displayed in the active table
        & in the export sheet

        LIMS-4162
        """
        self.info('create  Quantitative MiBi with unit')
        response, payload = self.test_unit_api.create_mibi_testunit(unit='%')
        self.assertEqual(response['status'], 1, payload)
        self.info('filter by test unit number: {}, to make sure that test unit created successfully'.
                  format(payload['number']))
        test_unit_found = self.test_units_page.filter_and_get_latest_row_data(payload['number'])
        self.assertTrue(test_unit_found['Unit'], '%')

        self.info(' * Download XSLX sheet')
        self.test_unit_page.download_xslx_sheet()
        values = self.test_unit_page.sheet.iloc[0].values
        fixed_sheet_row_data = self.fix_data_format(values)
        self.info('search for value of the unit field: {}'.format(test_unit_found['Unit']))
        self.assertIn(test_unit_found['Unit'], fixed_sheet_row_data)

    @skip('need API to take round option ID and returns round option name')
    def test032_edit_category_affects_testplan_step_two(self):
        """
        New: Test unit: Category Approach: Any update in test unit category should
        reflect in the test plan ( step two ) in this test unit

        LIMS-3687
        """
        self.info('Create new test unit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('create new test plan with created test unit with name {}'.format(payload['name']))

        test_plan = TestPlanAPI().create_testplan_from_test_unit_id(response['testUnit']['testUnitId'])
        self.assertTrue(test_plan, "Test plan not created")
        self.info('created test unit with number {}'.format(test_plan['number']))
        self.info('Navigate to test plan edit page and get test unit category')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        random_category_before_edit = self.test_plan.get_test_unit_category()
        self.assertEqual(random_category_before_edit, payload['selectedCategory'][0]['text'])
        self.info('edit newly created testunit with qualitative and random generated data')
        self.test_unit_page.open_test_unit_edit_page_by_id(response['testUnit']['testUnitId'])
        self.test_unit_page.sleep_small()
        new_random_category_edit = self.generate_random_string()
        self.info('update test unit category to {}'.format(new_random_category_edit))
        self.test_unit_page.set_category(new_random_category_edit)
        self.test_unit_page.save_and_wait()
        self.info('Navigate to test plan edit page and get test unit category')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        test_plan_category_after_edit = self.test_plan.get_test_unit_category()
        self.info('Assert that category updated successfully')
        self.assertEqual(test_plan_category_after_edit, new_random_category_edit)

    @skip('https://modeso.atlassian.net/browse/LIMSA-208')
    def test033_editing_limit_of_quantification_fields_should_affect_table_and_version(self):
        """
        New: Test unit: Limits of quantification Approach: Versions:In case I edit any field
        in the limits of quantification and press on save and create new version,
        new version should create & display in the active table & versions table

        LIMS-4423
        """
        self.info("get random quantitative test unit with qualtification limits only")
        random_testunit = random.choice(
            self.test_unit_api.get_testunit_with_quntification_limits_and_empty_specification())
        self.assertTrue(random_testunit, 'can not get random test unit')
        random_upper_limit = self.test_unit_page.generate_random_number(lower=50, upper=100)
        random_lower_limit = self.test_unit_page.generate_random_number(lower=0, upper=49)
        self.info('open the test unit in edit form to update it')
        self.test_unit_page.open_test_unit_edit_page_by_id(random_testunit['id'])
        self.test_unit_page.sleep_small()
        self.info('set upper limit to {}'.format(random_upper_limit))
        self.test_unit_page.set_quan_upper_limit(value=random_upper_limit)
        self.info('set lower limit to {}'.format(random_lower_limit))
        self.test_unit_page.set_quan_lower_limit(value=random_lower_limit)
        self.test_unit_page.sleep_tiny()
        self.test_unit_page.save_and_create_new_version()
        self.info('refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()
        self.assertEqual(self.test_unit_page.get_quan_upper_limit(), str(random_upper_limit))
        self.assertEqual(self.test_unit_page.get_quan_lower_limit(), str(random_lower_limit))
        self.info('making sure that two versions is created successfully')
        self.test_unit_page.get_test_units_page()
        test_unit_found, version_data = self.test_unit_page.filter_and_get_version(random_testunit['number'])
        self.info('version is {}, ant it should be {}'.format(test_unit_found['Version'],
                                                              str(random_testunit['version']+1)))

        self.assertEqual(test_unit_found['Version'], str(random_testunit['version']+1))
        self.assertEqual(test_unit_found['Quantification Limit'],
                         str(random_lower_limit) + '-' + str(random_upper_limit))
        self.info('assert that version data created sucesssfully')
        self.assertEqual(len(version_data), random_testunit['version']+1)
        self.assertEqual(version_data[-1]['Quantification Limit'],
                         str(random_lower_limit) + '-' + str(random_upper_limit))

    def test034_archived_testunit_should_not_appear_in_order(self):
        """
        Orders: Archived Test unit: Archive Approach: Archived test units
        shouldn't appear in orders in the drop down list

        LIMS-3710
        """
        self.info("get random archived test unit data")
        response, payload = self.test_unit_api.get_all_test_units(deleted="1")
        self.assertEqual(response['status'], 1, payload)
        archived_test_unit = random.choice(response['testUnits'])
        self.info("archived test unit data {}".format(archived_test_unit))
        self.info('create new order')
        self.info('get test unit suggestion list')
        Order().get_orders_page()
        if archived_test_unit['materialTypes'][0] != 'All':
            test_unit_suggetion_list = Order().create_new_order_get_test_unit_suggetion_list(
                material_type=archived_test_unit['materialTypes'][0], test_unit_name=archived_test_unit['name'])
        else:
            test_unit_suggetion_list = Order().create_new_order_get_test_unit_suggetion_list(
                material_type='', test_unit_name=archived_test_unit['name'])

        self.assertCountEqual(test_unit_suggetion_list, ['No items found'])

    def test035_can_not_archive_quantifications_limit_field(self):
        """
        New: Test unit: Configuration: Limit of quantification Approach: Display the new
        fields in the configuration section ( Upper limit & lower limit & unit of limit of
        quantification ) can't archived if used.

        LIMS-8309
        """
        self.test_unit_page.open_configurations()
        self.assertTrue(self.test_unit_page.archive_quantification_limit_field())
        validation_result = self.base_selenium.wait_element(element='test_units:archive_config_error')
        self.assertTrue(validation_result)

    @skip('waiting for API deleting')
    def test036_archive_quantifications_limit_field(self):
        """
        User can archive the quantification limits field from the configuration section if not used.
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
    def test037_restore_quantifications_limit_field(self):
        """
        User can archive the quantification limits field from the configuration section if not used.

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

    @attr(series=True)
    def test038_test_unit_name_is_mandatory(self):
        """
        New: Test unit: Configuration: Test unit Name Approach: Make the test units field
        as as mandatory field (This mean you can't remove it )

        LIMS- 5651
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.assertTrue(self.test_unit_page.check_all_options_of_search_view_menu())

    @parameterized.expand(['Name', 'Method', 'Type', 'No'])
    @attr(series=True)
    def test039_test_unit_name_allow_user_to_search_with_selected_options_testplan(self, search_view_option):
        """
        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with
        (name, number, type, method) in the drop down list of the test plan for.

        LIMS- 6422
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.select_option_to_view_search_with(view_search_options=[search_view_option])
        self.info('Create new testunit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new testunit created with number  {}'.format(payload['number']))
        self.info('get random In Progrees test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])

        if search_view_option == 'Name':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'Type':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'Method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)

    @attr(series=True)
    def test040_test_unit_name_search_default_options_name_type_in_testplan(self):
        """
        New: Test unit: Configuration: Test units field Approach: Allow name & type
        to display by default in the test plan form In case I select them from the
        test unit configuration

        LIMS-6423
        """
        # in set_configuration() I set search to be by name and type so I don't need to add this steps here
        self.info('Create new test unit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new test unit created with number  {}'.format(payload['number']))
        self.info('get random In Progress test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])
        self.assertTrue(is_name_exist)
        self.assertFalse(is_number_exist)
        self.assertTrue(is_type_exist)
        self.assertFalse(is_method_exist)

    @attr(series=True)
    def test041_test_unit_name_view_method_option_multiple_line_in_testplan(self):
        """
        New: Test Unit: Configuration: Test unit Name Approach: In case you select
        the method to display and you entered long text in it, the method should
        display into multiple lines (test plan)

        LIMS-6424
        """
        self.info('Generate random data for update')
        new_random_method = self.generate_random_string() + \
                            self.generate_random_string() + \
                            self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.test_unit_page.select_option_to_view_search_with(view_search_options=['Method'])
        self.info('Create new testunit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit(method=new_random_method)
        self.assertEqual(response['status'], 1, payload)
        self.info('new testunit created with number  {}'.format(payload['number']))
        self.info('get random In Progrees test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.set_test_unit(test_unit=new_random_method)
        multiple_lines_properties = self.test_plan.get_testunit_in_testplan_title_multiple_line_properties()
        self.assertEquals(multiple_lines_properties['textOverflow'], 'clip')
        self.assertEquals(multiple_lines_properties['lineBreak'], 'auto')

    @parameterized.expand([('Name', 'Type'),
                           ('Name', 'Method'),
                           ('Name', 'No'),
                           ('Type', 'Method'),
                           ('Type', 'No'),
                           ('Method', 'No')
                           ])
    @attr(series=True)
    def test042_test_unit_name_allow_user_to_search_with_selected_two_options_testplan(self, search_view_option1,
                                                                                       search_view_option2):
        """
        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with
        (name, number, type, method) in the drop down list of the analysis for

        LIMS- 6426
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.test_unit_page.select_option_to_view_search_with(
            view_search_options=[search_view_option1, search_view_option2])
        self.info('Create new test unit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new test unit created with number  {}'.format(payload['number']))
        self.info('get random In Progress test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])

        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Name' and search_view_option2 == 'Method':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'Name' and search_view_option2 == 'No':
            self.assertTrue(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Type' and search_view_option2 == 'Method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'Type' and search_view_option2 == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Method' and search_view_option2 == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)

    @skip('https://modeso.atlassian.net/browse/LIMSA-207')
    def test043_testunits_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        testunit_name = random.choice(self.test_unit_api.get_all_testunits_json())['name']
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
        Articles().get_articles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}articles'.format(self.base_selenium.url))

    @skip('https://modeso.atlassian.net/browse/LIMSA-212')
    def test044_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        self.assertFalse(self.test_unit_page.deselect_all_configurations())

    @parameterized.expand([('number', 'testunit_number_filter', 'Test Unit No.'),
                           ('name', 'testunit_name_filter', 'Test Unit Name'),
                           ('method', 'method_filter', 'Method'),
                           ('createdAt', 'filter_created_at', 'Created On')])
    def test045_filter_by_testunit_text_fields(self, filter_case, filter, header_name):
        """
        New: Test units: Filter Approach: Make sure you can filter by test unit no
        LIMS-6430

        New: Test units: Filter Approach: Make sure you can filter by name
        LIMS-6432

        New: Test units: Filter Approach: Make sure you can filter by method
        LIMS-6434

        New: Test units: Filter Approach: Make sure you can filter by created on
        LIMS-6431
        """
        data_to_filter_with = self.test_unit_api.get_first_record_with_data_in_attribute(attribute=filter_case)
        self.assertNotEqual(data_to_filter_with, False)

        if filter_case == 'createdAt':
            data_to_filter_with = self.test_unit_page.convert_to_dot_date_format(date=data_to_filter_with)

        self.info('filter with {}'.format(data_to_filter_with))
        self.test_unit_page.apply_filter_scenario(filter_element='test_units:{}'.format(filter),
                                                  filter_text=data_to_filter_with, field_type='text')

        table_records = self.test_unit_page.result_table()[:-1]

        for record in table_records:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)
            self.assertIn(str(data_to_filter_with), row_data[header_name].replace("'", ""))

    def test046_filter_by_testunit_unit_returns_only_correct_results(self):
        """
        New: Test units: Filter Approach: Make sure you can filter by unit

        LIMS-6427
        """
        data_to_filter_with = self.test_unit_api.get_first_record_with_data_in_attribute(attribute='unit')
        self.assertNotEqual(data_to_filter_with, False)
        self.info('filter with {}'.format(data_to_filter_with))

        self.test_unit_page.apply_filter_scenario(filter_element='test_unit:spec_unit',
                                                  filter_text=data_to_filter_with, field_type='text')
        table_records = self.test_unit_page.result_table()
        del table_records[-1]
        for record in table_records:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)
            self.assertEqual(
                row_data['Unit'].replace("'", ""),
                str(data_to_filter_with.replace('{', '').replace('}', '').replace('[', '').replace(']', '')))

    @parameterized.expand([('categoryName', 'filter_category', 'Category'),
                           ('typeName', 'filter_Type', 'Type')])
    def test047_filter_by_testunit_drop_down_fields(self, filter_case, filter, header_name):
        """
        New: Test units: Filter Approach: Make sure you can filter by category
        LIMS-6429

        New: Test units: Filter Approach: Make sure you can filter by type
        LIMS-6435
        """
        data_to_filter_with = self.test_unit_api.get_first_record_with_data_in_attribute(attribute=filter_case)
        self.assertNotEqual(data_to_filter_with, False)
        self.info('filter with {}'.format(data_to_filter_with))
        self.test_unit_page.apply_filter_scenario(filter_element='test_units:{}'.format(filter),
                                                  filter_text=data_to_filter_with)
        table_records = self.test_unit_page.result_table()

        del table_records[-1]
        for record in table_records:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)
            self.assertIn(str(data_to_filter_with), row_data[header_name].replace("'", ""))

    def test048_filter_by_testunit_material_type_returns_only_correct_results(self):
        """
        New: Test units: Filter Approach: Make sure you can filter by material type
        LIMS-6433
        """
        data_to_filter_with = self.test_unit_api.get_first_record_with_data_in_attribute(attribute='materialTypes')
        self.assertNotEqual(data_to_filter_with, False)
        self.info('filter with {}'.format(data_to_filter_with[0]))
        self.test_unit_page.apply_filter_scenario(filter_element='test_units:filter_material_type',
                                                  filter_text=data_to_filter_with[0])
        table_records = self.test_unit_page.result_table()
        del table_records[-1]
        for record in table_records:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)
            testunit_material_types = row_data['Material Type'].split(',')
            self.assertIn(str(data_to_filter_with[0]), testunit_material_types)

    @attr(series=True)
    def test049_filter_by_testunit_changed_by(self):
        """
        New: Test units: Filter Approach: Make sure you can filter by changed by

        LIMS-6428
        """
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_units_page.get_test_units_page()
        new_name = self.generate_random_string()
        method = self.generate_random_string()
        test_unit_no = self.test_unit_page.create_qualitative_testunit(name=new_name, method=method)
        self.test_unit_page.save_and_wait()
        self.assertTrue(test_unit_no, 'Test unit not created')
        self.info('New unit is created successfully with number: {}'.format(test_unit_no))
        self.test_units_page.sleep_tiny()
        test_unit_found = self.test_units_page.filter_by_user_get_result(payload['username'])
        self.assertTrue(test_unit_found)

