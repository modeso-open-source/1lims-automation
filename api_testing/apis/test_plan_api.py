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

    def get_completed_testplans(self):
        response = self.get_all_test_plans()
        all_test_plans = response.json()['testPlans']
        completed_test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == 'Completed']
        return completed_test_plans

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
                self.restore_testplans(ids=[id])
                return False
        else:
            return False
