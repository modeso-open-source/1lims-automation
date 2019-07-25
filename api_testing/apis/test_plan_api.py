from api_testing.apis.base_api import BaseAPI


class TestPlanAPI(BaseAPI):
    def testplans_list_table(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['testplans_list_table'])
        _payload = {'sort_value': 'id',
                    'limit': 5,
                    'start': 0,
                    'sort_order': 'asc',
                    'filter': '{"id":2440}'}
        payload = self.update_payload(_payload, **kwargs)
        return self.session.get(api, data=payload)
