from api_testing.apis.base_api import BaseAPI


class OrdersAPI(BaseAPI):
    def get_all_orders(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['list_all_orders'])
        _payload = {"sort_value": "createdAt",
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

    def get_order_by_id(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_order_by_id'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def create_new_order(self, **kwargs):
        request_body = {}
        request_body['deletedTestPlans'] = []
        request_body['deletedAnalysisIds'] = []
        request_body['dynamicFieldsValues'] = []
        request_body['analysisNo'] = []
        request_body['selectedDepartments'] = []
        request_body['orderType'] = {
            'id': 1,
            'text': 'New Order'
        }
        request_body['yearOption'] = 1

        if 'attachments' not in kwargs:
            request_body['attachments'] = []
        if 'testPlans' in kwargs:
            request_body['testPlans'] = kwargs['testPlans']
            selected_testplan_arr = []
            for testplan in request_body['testPlans']:
                selected_testplan_arr.append({
                    'id': testplan['id'],
                    'name': testplan['text'],
                    'version': ''
                })
                
            request_body['selectedTestPlans'] = selected_testplan_arr

        for key in kwargs:
            request_body[key] = kwargs[key]

        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['create_article']) 
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=request_body, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()

        if data['status'] == 1:
            return data['article']
        else:
            return data['message']