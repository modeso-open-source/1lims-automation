from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory
import json, os


class AnalysisAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_analysis(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['analysis_api']['list_all_analysis'])
        _payload = {"sort_value": "no",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('put')
    def archive_analysis(self, analysis_id):
        """
        If success, response['message'] == 'operation_success'
        :param analysis_id:
        :return:
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['analysis_api']['archive_analysis'], str(analysis_id)) 
        return api, {}

    @api_factory('put')
    def restore_analysis(self, analysis_id):
        """
        If success, response['message'] == 'operation_success'
        :param analysis_id:
        :return:
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['analysis_api']['restore_analysis'], str(analysis_id)) 
        return api, {}

    @api_factory('delete')
    def delete_analysis(self, analysis_id):
        """
        If success, response['message'] == 'hard_delete_success'
        :param analysis_id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['analysis_api']['delete_analysis'], str(analysis_id)) 
        return api, {}

class AnalysisAPI(AnalysisAPIFactory):
    def set_filter_configuration(self):
        self.info('set order filter configuration')
        config_file = os.path.abspath('api_testing/config/analysis_filter_config.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_filter_configuration(payload=payload, module='orders_api')
