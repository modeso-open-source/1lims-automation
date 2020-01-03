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
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['delete_testunits'], str(id)) 
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
            api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['delete_testunits'], str(id)) 
            self.info('DELETE : {}'.format(api))
            response = self.session.delete(api, params='', headers=self.headers, verify=False)
            self.info('Status code: {}'.format(response.status_code))
            data = response.json()
            if data['status'] == 1 and data['message']=='hard_delete_success':
                return True
            else:
                return False
        else:
            return False