from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


class TestPlanAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_test_plans(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_all_test_plans'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def _get_testunits_in_testplan(self, id):
        """
        If success, testunits = response['testPlan']['specifications']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['get_testunits_in_testplan'], id)
        return api, {}

    @api_factory('get')
    def get_testplan_testunits(self, id=1):
        """
        if success, response['specifications']
        :param id:
        :return:
        """
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_testplan_testunits'])
        _payload = {"sort_value": "id",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": '{"id": ' + str(id) + '}'
                    }
        return api, _payload

    @api_factory('get')
    def _get_testplan_form_data(self, id=1):
        """
        if success, response['testPlan']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['form_data'], str(id))
        return api, {}

    @api_factory('put')
    def archive_testplans(self, ids=['1']):
        """
        if success, response['message'] == 'delete_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_plan_api']['archive_testplans'], ','.join(ids))
        return api, {}

    @api_factory('put')
    def restore_testplans(self, ids=['1']):
        """
        if success, response['message']=='restore_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_plan_api']['restore_testplans'], ','.join(ids))
        return api, {}

    @api_factory('delete')
    def delete_archived_testplan(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['delete_testplan'], str(id))
        return api, {}

    @api_factory('post')
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
        return api, {}

    @api_factory('get')
    def list_testunit_by_name_and_material_type(self, materialtype_id, name='', negelectIsDeleted=0,
                                                searchableValue=''):
        """
        if success, response['testUnits]
        :param materialtype_id:
        :param name:
        :param negelectIsDeleted:
        :param searchableValue:
        :return:
        """
        api = '{}{}{}?name={}&negelectIsDeleted={}&searchableValue={}'.format(self.url,
                                                                              self.END_POINTS['test_unit_api'][
                                                                                  'list_testunit_by_name_and_materialtype'],
                                                                              materialtype_id, name, negelectIsDeleted,
                                                                              searchableValue)
        return api, {}


class TestPlanAPI(TestPlanAPIFactory):
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

    def get_testplans_with_status(self, status):
        all_test_plans = self.get_all_test_plans_json()
        test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == status]
        return test_plans

    def get_testunits_in_testplan(self, id=1):
        response, _ = self._get_testunits_in_testplan(id)
        return response['testPlan']['specifications']

    def get_testplan_with_quicksearch(self, quickSearchText, **kwargs):
        filter_text = '{"quickSearch":"' + quickSearchText + '","columns":["number","name"]}'
        response, _ = self.get_all_test_plans(filter=filter_text, **kwargs)
        return response['testPlans']

    def get_testplan_with_filter(self, filter_option, filter_text, **kwargs):
        filter_text = '{"' + filter_option + '":"' + filter_text + '","columns":["number","name"]}'
        response, _ = self.get_all_test_plans(filter=filter_text, start=0, **kwargs)
        return response['testPlans']

    def get_testplan_form_data(self, id=1):
        response, _ = self._get_testplan_form_data(id)
        return response['testPlan']

    def delete_active_testplan(self, id=1):
        if self.archive_testplans(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_testplan(id=id)[0]['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_testplans(ids=[str(id)])
                return False
        else:
            return False