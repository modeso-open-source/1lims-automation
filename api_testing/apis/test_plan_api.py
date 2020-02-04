from api_testing.apis.base_api import BaseAPI


class TestPlanAPI(BaseAPI):
    def get_all_test_plans(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_all_test_plans'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_all_test_plans_json(self, **kwargs):
        testplans_response = self.get_all_test_plans(**kwargs)
        return testplans_response.json()['testPlans']

    def get_completed_testplans(self, **kwargs):
        response = self.get_all_test_plans(**kwargs)
        all_test_plans = response.json()['testPlans']
        completed_test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == 'Completed']
        return completed_test_plans
    
    def get_inprogress_testplans(self, **kwargs):
        response = self.get_all_test_plans(**kwargs)
        all_test_plans = response.json()['testPlans']
        inprogress_test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == 'InProgress']
        return inprogress_test_plans

    def get_testunits_in_testplan(self, id):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['get_testunits_in_testplan'], id)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        testplan_data = response.json()['testPlan']
        testunits_data = testplan_data['specifications']
        return testunits_data

    def get_testplan_with_quicksearch(self, quickSearchText, **kwargs):
        filter_text = '{"quickSearch":"' + quickSearchText + '","columns":["number","name"]}'
        response = self.get_all_test_plans(filter=filter_text, **kwargs)
        return response.json()['testPlans']

    def get_testplan_with_filter(self, filter_option, filter_text, **kwargs):
        filter_text = '{"' + filter_option + '":"' + filter_text + '","columns":["number","name"]}'
        response = self.get_all_test_plans(filter=filter_text, start=0, **kwargs)
        return response.json()['testPlans']
    
    def get_all_test_plans_json(self, **kwargs):
        testplans_response = self.get_all_test_plans(**kwargs)
        return testplans_response.json()['testPlans']

    def get_testplan_testunits(self, id=1):
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_testplan_testunits'])
        _payload = {"sort_value": "id",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": '{"id": '+str(id)+'}'}
        
        # payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=_payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['specifications']
        return response.json()

    def get_testplan_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testPlan']
        else:
            return False
    
    def archive_testplans(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_plan_api']['archive_testplans'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_testplans(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_plan_api']['restore_testplans'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='restore_success':
            return True
        else:
            return False
    
    def delete_archived_testplan(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['delete_testplan'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_testplan(self, id=1):
        if self.archive_testplans(ids=[str(id)]):
            if self.delete_archived_testplan(id=id):
                return True
            else:
                self.restore_testplans(ids=[str(id)])
                return False
        else:
            return False
    
    # example for using testplan creation using the API 
    # article = self.article_api.list_articles_by_materialtype(materialtype_id=1)[0]
    # material_type = self.general_utilities_api.list_all_material_types()[0]
    # testunit = self.test_unit_api.get_all_test_units().json()['testUnits'][0]
    # testunit_form_data = self.test_unit_api.get_testunit_form_data(id=int(testunit['id']))
    # testunit = self.test_unit_page.map_testunit_to_testplan_format(testunit=testunit_form_data)

    # testplan_name = self.test_unit_page.generate_random_text()
    # testplan_number = self.test_unit_page.generate_random_number()
    # testplan_object = {
    #     'text': testplan_name,
    #     'id': 'new'
    # }
    # self.base_selenium.LOGGER.info(self.test_plan_api.create_testplan(number=testplan_number, testPlan=testplan_object, materialType=material_type, selectedArticles=[article], testUnits=[testunit]))
    def create_testplan(self, **kwargs):
        """
        NOTE: calling this api without adding testunits, will create an in progress testplan, to create a complete testplan
        you will need to pass parameter testunits[testunit_object], and this object is can be formated by the following steps,
        
        testunit = self.test_unit_api.get_testunit_form_data(id=#testunit_id)
        formated_testunit = self.test_unit_page.map_testunit_to_testplan_format(testunit=testunit)
        self.test_plan_api.create_testplan(testunits=[formated_testunit])

        param: testplan: {
            'id': testplan id, 'new' in case of new testplan name,
            'text': testplan name text
        }
        param: 'number': testplan number
        param: 'selectedArticles':  denotes articles that support this testplan, all by default[{
            'id': article id,
            'text': article name
        }]
        param: materialType: testplan material type, raw material by default{
            'id': material type id,
            'text': material type text
        }
        param testUnits: testunits in this testplan, if empty, it will be created as in progress testplan, else
        put array of testunits by the following way
        using testunit id, select testunit form data through api call: test_unit_api.get_testunit_form_data(id=#testunit_id)
        and then use the return of this mapping function test_unit_page.map_testunit_to_testplan_format(testunit=formdata_testunit) to add it to the testunits array
        """
        testplan_name = self.generate_random_string()
        _payload = {
            'number': self.generate_random_number(),
            'testPlan': {
                'id': 'new',
                'text': testplan_name
            },
            'selectedTestPlan': {
                'id': 'new',
                'text': testplan_name
            },
            'selectedArticles': [{
                'id': -1,
                'text': 'All'
            }],
            'materialType': {
                'id': 1,
                'text': 'Raw Material'
            },
            'attachments': '[]',
            'selectedTestUnits': [],
            'materialTypeId': 1,
            'dynamicFieldsValues': [],
            'testUnits': []
        }   

        
        payload = self.update_payload(_payload, **kwargs)
        if 'testPlan' in kwargs:
            payload['selectedTestPlan'] = [kwargs['testPlan']]
        if 'materialType' in kwargs:
            payload['materialTypeId'] = kwargs['materialType']['id']
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['create_testplan']) 
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



