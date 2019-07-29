from api_testing.apis.base_api import BaseAPI


class TestUnitAPI(BaseAPI):
    def get_all_test_units(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_all_test_units'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers)
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
        response = self.session.get(api, params=payload, headers=self.headers)
        self.info('Status code: {}'.format(response.status_code))
        return response
