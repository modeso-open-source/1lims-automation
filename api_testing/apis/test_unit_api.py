from api_testing.apis.base_api import BaseAPI

class TestUnitAPI(BaseAPI):
    def get_all_test_units(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_all_test_units'])
        _payload = {"sort_value": "number",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def report_sheet_get_list_table(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['report_sheet_get_list_table'])
        _payload = {'sort_value': 'id',
                    'limit': 5,
                    'start': 0,
                    'sort_order': 'asc',
                    'filter': '{"id":2440}'}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_all_testunits_json(self):
        testunits = self.get_all_test_units().json()['testUnits']
        return testunits

    def get_testunit_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['form_data'], str(id))
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testUnit']
        else:
            return False

    def archive_testunits(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_unit_api']['archive_testunits'], ','.join(ids))
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False

    def restore_testunits(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_unit_api']['restore_testunits'], ','.join(ids))
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='operation_success':
            return True
        else:
            return False

    def delete_archived_testunit(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['delete_testunit'], str(id))
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_testunit(self, id=1):
        if self.archive_testunits(ids=[str(id)]):
            if self.delete_archived_testunit(id=id):
                return True
            else:
                self.restore_testunits(ids=[str(id)])
                return False
        else:
            return False

    def list_testunits_types(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_types'])
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        return data

    def list_testunits_concentrations(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_concentrations'])
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        return data['concentrations']


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
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()

        if data['status'] == 1:
            return payload
        else:
            return data['message']

    def create_quantitative_testunit(self, **kwargs):
        random_category =self.generate_random_string()
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
                'text': 'All'
            }],
            'textValueArray': [],
            'textValue': '',
            'upperLimit': self.generate_random_number(lower=50, upper=100),
            'lowerLimit': self.generate_random_number(lower=1, upper=49),
            'method': self.generate_random_string(),
            'quantificationUpperLimit': '',
            'quantificationLowerLimit': '',
            'useSpec': True,
            'iterations': '1'
        }
        payload = self.update_payload(_payload, **kwargs)
        if 'category' in kwargs:
            payload['selectedCategory'] = [kwargs['category']]

        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['create_testunit'])
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()

        if data['status'] == 1:
            return payload
        else:
            return data['message']



    def create_mibi_testunit(self, **kwargs):

        random_category =self.generate_random_string()
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
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()

        if data['status'] == 1:
            return payload
        else:
            return data['message']

    def list_testunit_by_name_and_material_type(self, materialtype_id, name='', negelectIsDeleted=0, searchableValue=''):
        api = '{}{}{}?name={}&negelectIsDeleted={}&searchableValue={}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_by_name_and_materialtype'], materialtype_id, name, negelectIsDeleted, searchableValue)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testUnits']
        return []

    def get_testunit_with_empty_specification(self):
        testunits_request = self.get_all_test_units(filter='{"typeName":2}').json()
        testunits = testunits_request['testUnits']
        testunits_name = []
        for testunit in testunits:
            if testunit['specifications'] == '':
                testunits_name.append(testunit['name'])
        return testunits_name