from api_testing.apis.base_api import BaseAPI


class AnalysisAPI(BaseAPI):
    def get_all_orders(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['analysis_api']['list_all_analysis'])
        _payload = {"sort_value": "no",
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
    
    def archive_analysis(self, analysis_id):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['analysis_api']['archive_analysis'], str(analysis_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'operation_success':
            return True
        else:
            return False
    
    def restore_analysis(self, analysis_id):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['analysis_api']['restore_analysis'], str(analysis_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'operation_success':
            return True
        else:
            return False
    
    def delete_analysis(self, analysis_id):
        api = '{}{}{}'.format(self.url, self.END_POINTS['analysis_api']['delete_analysis'], str(analysis_id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'hard_delete_success':
            return True
        else:
            return False