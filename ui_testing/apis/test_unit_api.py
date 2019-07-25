from ui_testing.apis.base_api import BaseAPI


class TestUnitAPI(BaseAPI):
    def report_sheet_get_list_table(self, **kwargs):
        api = self.url + "/api/reportSheets/get/list/table/testunits"
        data = {'sort_value': 'id',
                'limit': 5,
                'start': 0,
                'sort_order': 'asc',
                'filter': '{"id":2440}'}
        data = self.update_data(data, **kwargs)
        return self.session.get(api, data=data)
