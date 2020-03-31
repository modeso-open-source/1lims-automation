from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


class GeneralUtilitiesAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_permissions(self):
        api = '{}{}'.format(self.url, self.END_POINTS['components']['list_components'])
        return api, {}

    @api_factory('get')
    def list_all_material_types(self):
        """
        if success, response['materialTypes]
        :return: response, payload
        """
        api = '{}{}'.format(self.url, self.END_POINTS['materialTypes']['list_material_types']) 
        return api, {}


class GeneralUtilitiesAPI(GeneralUtilitiesAPIFactory):
    @staticmethod
    def map_component_to_permission(component):
        return {
            'id': component['id'],
            'name': component['name'],
            'view': False,
            'modify': False
        }

    def list_all_permissions(self):
        response = self.get_all_permissions()
        if response['status'] == 1:
            permissions_list = []
            components = response['components']
            for component in components:
                permissions_list.append(self.map_component_to_permission(component=component))
                for item in component['items']:
                    permissions_list.append(self.map_component_to_permission(component=item))
            return permissions_list
        return []
