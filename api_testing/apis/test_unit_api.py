from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
import random, json, os


class TestUnitAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_test_units(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_all_test_units'])
        _payload = {"sort_value": "number",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"
                    }
        #for key in kwargs:
         #   if key in _payload.keys():
          #      _payload[key] = kwargs[key]
        return api, _payload

    @api_factory('get')
    def report_sheet_get_list_table(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['report_sheet_get_list_table'])
        _payload = {'sort_value': 'id',
                    'limit': 5,
                    'start': 0,
                    'sort_order': 'asc',
                    'filter': '{"id":2440}'
                    }
        return api, {}

    @api_factory('get')
    def get_testunit_form_data(self, id=1):
        """
        if success, response['testUnit']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['form_data'], str(id))
        return api, {}

    @api_factory('get')
    def get_auto_generated_testunit_no(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['get_auto_generated_number'])
        return api, {}

    @api_factory('put')
    def archive_testunits(self, ids=['1']):
        """"
        if success, response['message'] == 'delete_success'
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_unit_api']['archive_testunits'], ','.join(ids))
        return api, {}

    @api_factory('put')
    def restore_testunits(self, ids=['1']):
        """
         if success, response['message']=='operation_success'
         :param ids:
         :return:
         """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_unit_api']['restore_testunits'], ','.join(ids))
        return api, {}

    @api_factory('delete')
    def delete_archived_testunit(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['delete_testunit'], str(id))
        return api, {}

    @api_factory('get')
    def list_testunits_types(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_types'])
        return api, {}

    @api_factory('get')
    def list_testunits_concentrations(self):
        """
        if success, response['concentrations']
        :return:
        """
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_concentrations'])
        return api, {}

    @api_factory('get')
    def list_testunit_by_name_and_material_type(self, materialtype_id, name='', negelectIsDeleted=0, searchableValue=''):
        """
        if success, response['testUnits']
        """
        api = '{}{}{}?name={}&negelectIsDeleted={}&searchableValue={}'.format(
            self.url, self.END_POINTS['test_unit_api']['list_testunit_by_name_and_materialtype'],
            materialtype_id, name, negelectIsDeleted, searchableValue)
        return api, {}

    """
    NOTE testunits created without specific data, random data will be assigned, and in case of material type, All is assigned, and in case of iteration, 1 is assigned
    NOTE you can get a list of materialtypes using the API call general_utilities_api.list_all_material_types()
    
    NOTE in case of using quantification limit only testunit, you have to assign the following attributes with the corresponding values
    
    parameter: number: testunit number
    parameter: name: testunit name
    useSpec: False,
    upperLimit: '',
    lowerLimit: ''

    Parameter: selectedMaterialTypes: [{

        'id': material type id,
        'text': material type text
        }]
    Parameter: category: {
        'id': 'new' in case of creating new category, category id in case of old category
        'text': category text
        }
    Parameter: type: {
        'id': testunit type id can be obtained using API call list_testunits_types,
        'text': testunit type text
        }
    Parameter: unit: *optional*
    Parameter: method: mandatory field, will be set to 'random method' in case no method provided
    Parameter: textValue: string separated by ',' dentoes the values of specifications (in case of qualtiative testunit only)
    Parameter: useQuantification: True/False in case of Quantitative testunits with quantification limit 
    Parameter: useSpec: True/False in case of Quantitative testunits with specifications
    Parameter: upperLimit: specification upper limit in case of Quantitative with specifications
    Parameter: lowerLimit: specification lower limit in case of Quantitative with specifications
    Parameter: quantificationUpperLimit: quantification upper limit in case of Quantitative with quantification
    Parameter: quantificationLowerLimit: quantification lower limit in case of Quantitative with quantification
    Parameter: quantificationUnit: unit in case of quantification limit
    Parameter: selectedConcs: [{
        'id': concentration id, can be obtained using list_testunits_concentrations,
        'text': concentration text, can be obtained using list_testunits_concentrations
        }]
    in case of MiBi, use upperLimit: to define mibi upper limit value
    """

    @api_factory('post')
    def create_qualitative_testunit(self, **kwargs):
        random_category = self.generate_random_string()
        _payload = {
            'name': self.generate_random_string(),
            'number': self.generate_random_number(),
            'selectedConcs': [],
            'unit': '',
            'dynamicFieldsValues': [],
            'type': {
                'id': 1,
                'text': "Qualitative"
            },
            'testUnitTypeId': 1,
            'category': {
                'id': 'new',
                'text': random_category
            },
            'selectedCategory': [{
                'id': 'new',
                'text': random_category
            }],
            'selectedMaterialTypes': [{
                'id': 0,
                'text': 'All'
            }],
            'method': self.generate_random_string(),
            'iterations': '1'
        }
        payload = self.update_payload(_payload, **kwargs)

        if 'textValue' not in kwargs:
            payload['textValue'] = self.generate_random_string()

        qualitiative_values = payload['textValue'].split(',')
        values_arr = []
        for value in qualitiative_values:
            values_arr.append({
                'display': value,
                'value': value
            })
        payload['textValueArray'] = values_arr
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['create_testunit'])
        return api, payload

    @api_factory('post')
    def create_quantitative_testunit(self, **kwargs):
        """
        if you want to create  quantitative test unit with Quantification limits you should call
        create_quantitative_testunit(useSpec=False, useQuantification=True,
                                     quantificationUpperLimit=upperLimit,
                                     quantificationLowerLimit=lowerLimit)

        """
        random_category = self.generate_random_string()
        _payload = {
            'name': self.generate_random_string(),
            'number': self.generate_random_number(),
            'selectedConcs': [],
            'dynamicFieldsValues': [],
            'type': {
                'id': 2,
                'text': "Quantitative"
            },
            'testUnitTypeId': 2,
            'category': {
                'id': 'new',
                'text': random_category
            },
            'selectedCategory': [{
                'id': 'new',
                'text': random_category
            }],
            'selectedMaterialTypes': [{
                'id': 0,
                'text': 'All'}],
            'textValueArray': [],
            'textValue': '',
            'upperLimit': self.generate_random_number(lower=50, upper=100),
            'lowerLimit': self.generate_random_number(lower=1, upper=49),
            'method': self.generate_random_string(),
            'quantificationUpperLimit': '',
            'quantificationLowerLimit': '',
            'useSpec': True,
            'unit': '',
            'iterations': '1',
            "roundingOption": {"id": 0, "text": "No Rounding"}
        }
        payload = self.update_payload(_payload, **kwargs)
        if 'category' in kwargs:
            payload['selectedCategory'] = [kwargs['category']]

        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['create_testunit'])
        return api, payload

    @api_factory('post')
    def create_mibi_testunit(self, **kwargs):
        random_category = self.generate_random_string()
        _payload = {
            'name': self.generate_random_string(),
            'number': self.generate_random_number(),
            'selectedConcs': [{
                'id': 1,
                'text': '1:10'
            }],
            'dynamicFieldsValues': [],
            'type': {
                'id': 3,
                'text': "Quantitative MiBi"
            },
            'testUnitTypeId': 3,
            'category': {
                'id': 'new',
                'text': random_category
            },
            'selectedCategory': [{
                'id': 'new',
                'text': random_category
            }],
            'selectedMaterialTypes': [{
                'id': 0,
                'text': 'All'
            }],
            'textValueArray': [],
            'textValue': '',
            'upperLimit': self.generate_random_number(lower=50, upper=100),
            'method': self.generate_random_string(),
            'iterations': '1'
        }
        payload = self.update_payload(_payload, **kwargs)
        if 'category' in kwargs:
            payload['selectedCategory'] = [kwargs['category']]

        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['create_testunit'])
        return api, payload


class TestUnitAPI(TestUnitAPIFactory):
    def get_all_testunits_json(self):
        response, _ = self.get_all_test_units()
        testunits = response['testUnits']
        return testunits

    def get_testunit_with_quicksearch(self, quickSearchText, **kwargs):
        filter_text = '{"quickSearch":"' + quickSearchText + '","columns":["number","name"]}'
        response, _ = self.get_all_test_units(filter=filter_text, **kwargs)
        if response['count'] >= 1:
            return response['testUnits']
        else:
            return None

    def get_test_unit_with_spec_or_quan_only(self, spec_or_quan):
        response, _ = self.get_all_test_units(filter='{"typeName":2}')
        testunits = response['testUnits']
        for testunit in testunits:
            if spec_or_quan == 'spec' and testunit['specifications'] != '' and testunit['quantification'] == '':
                return testunit['id']
            elif spec_or_quan == 'quan' and testunit['specifications'] == '' and testunit['quantification'] != '':
                return testunit['id']

    def get_first_record_with_data_in_attribute(self, attribute):
        testunits_request, _ = self.get_all_test_units()
        if (testunits_request['status'] != 1) or (testunits_request['count'] == 0):
            return False
        testunit_records = testunits_request['testUnits']
        for testunit in testunit_records:
            if testunit[attribute] != '':
                return testunit[attribute]
        
    def get_testunit_with_empty_specification(self):
        testunits_request, _ = self.get_all_test_units(filter='{"typeName":2}')
        testunits = testunits_request['testUnits']
        testunits_name = []
        for testunit in testunits:
            if testunit['specifications'] == '':
                testunits_name.append(testunit['name'])
        return testunits_name

    def get_testunit_with_quntification_limits_and_empty_specification(self):
        testunits_request, _ = self.get_all_test_units(filter='{"typeName":2}')
        testunits = testunits_request['testUnits']
        testunits_list = []
        for testunit in testunits:
            if testunit['specifications'] == '' and testunit['quantification'] not in ['', '-*-', '-']:
                testunits_list.append(testunit)
        return testunits_list

    def delete_active_testunit(self, id=1):
        if self.archive_testunits(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_testunit(id=id)[0]['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_testunits(ids=[str(id)])
                return False
        else:
            return False

    def get_testunits_with_material_type(self, material_types='Raw Material'):
        all_test_units, _ = self.get_all_test_units()
        test_units = all_test_units['testUnits']
        selected_test_units = [test_unit for test_unit in test_units if test_unit['materialTypes'] == [material_types]]
        return selected_test_units

    def get_test_unit_name_with_value_with_material_type(self, material_type,
                                                         avoid_duplicate=False, duplicated_test_unit=''):

        material_id = GeneralUtilitiesAPI().get_material_id(material_type)
        testunits = TestUnitAPI().list_testunit_by_name_and_material_type(materialtype_id=material_id)[0]['testUnits']

        if avoid_duplicate:  # make sure test unit differs from old one
            testunits = [testunit for testunit in testunits if testunit['name'] != duplicated_test_unit]
        testunits_with_values = []  # make sure test unit have value
        for testunit in testunits:
            if testunit['typeName'] == 'Quantitative MiBi' and testunit['mibiValue'] and testunit['concentrations']:
                testunits_with_values.append(testunit)
            elif testunit['typeName'] == 'Quantitative':
                if testunit['lowerLimit'] or testunit['upperLimit']:
                    testunits_with_values.append(testunit)
            elif testunit['typeName'] == 'Qualitative' and testunit['textValue']:
                testunits_with_values.append(testunit)

        if not testunits_with_values:
            self.info(" No test unit with req. material type, so create one")
            api, testunit_payload = self.create_quantitative_testunit()
            if api('status') == 1:
                return testunit_payload
        else:
            testunit = random.choice(testunits_with_values)
            return testunit

    def get_testplan_valid_test_unit(self):
        test_units, payload = self.get_all_test_units(limited=20, filter='{"materialTypes":"all"}')
        testunits_with_values = []  # make sure test unit have value
        for testunit in test_units['testUnits']:
            if testunit['typeName'] == 'Quantitative':
                if testunit['specifications'] or testunit['quantification']:
                    testunits_with_values.append(testunit)
            elif testunit['typeName'] == 'Qualitative' and testunit['specifications']:
                testunits_with_values.append(testunit)

        return testunits_with_values

    def get_unit_format(self, test_unit_no):
        test_unit = self.get_testunit_with_quicksearch(test_unit_no.replace("'", ""))
        if test_unit:
            return test_unit[0]['unit']

    def create_test_unit_with_multiple_material_types(self, type='Qualitative'):
        response, _ = GeneralUtilitiesAPI().list_all_material_types()
        material_type = random.choices(response['materialTypes'], k=4)
        if type == 'Quantitative MiBi':
            api, payload = self.create_mibi_testunit(selectedMaterialTypes=material_type)
        elif type == 'Quantitative':
            api, payload = self.create_quantitative_testunit(selectedMaterialTypes=material_type)
        elif type == 'Qualitative':
            api, payload = self.create_qualitative_testunit(selectedMaterialTypes=material_type)

        test_unit_dict = {'id': api['testUnit']['testUnitId']}
        test_unit_dict.update(payload)
        if api['status'] == 1:
            return test_unit_dict
        else:
            return None

    def create_test_unit_with_long_text(self):
        self.info('Generate random data for update')
        long_txt = ''.join([self.generate_random_string() for _ in range(5)])
        api, testunit_payload = self.create_qualitative_testunit(method=long_txt)
        return api, testunit_payload

    def get_testunits_material_types(self, testunits=[]):
        testunit_materials = []
        for testunit in testunits:
            testunit_info = self.get_testunit_with_quicksearch(quickSearchText=testunit)
            if testunit_info is not None:
                for tu in testunit_info:
                    testunit_materials.append(tu['materialTypes'][0])
        return testunit_materials

    def set_configuration(self):
        self.info('set test unit configuration')
        config_file = os.path.abspath('api_testing/config/testUnit.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)

    def set_name_configuration_unit_only(self):
        self.info('set test unit configuration')
        config_file = os.path.abspath('api_testing/config/testUnit_unit.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)

    def set_name_configuration_name_only(self):
        self.info('set test unit configuration')
        config_file = os.path.abspath('api_testing/config/testUnit_name.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)
