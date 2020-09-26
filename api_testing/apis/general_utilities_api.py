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

    @api_factory('put')
    def enable_article(self, **kwargs):
        payload = {
               "entityId": 2,
               "status": True,
               "id": 1
            }
        api = '{}{}'.format(self.url, self.END_POINTS['modules']['disable_article'])
        return api, payload

    @api_factory('get')
    def has_articles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['modules']['has_articles'])
        return api, {}

    @api_factory('get')
    def get_configuration(self):
        api = f'{self.url}{self.END_POINTS["field_data"]["get_configuration"]}'
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

    def get_material_id(self, material_type):
        all_materials, _ = self.list_all_material_types()
        for material in all_materials['materialTypes']:
            if material['name'] == material_type:
                return material['id']

    def get_material_types_without_duplicate(self, old_material):
        all_materials, _ = self.list_all_material_types()
        material_without_duplicate = []
        for material in all_materials['materialTypes']:
            if material['name'] != old_material:
                material_without_duplicate.append(material['name'])
        return material_without_duplicate

    def get_formatted_material_types_without_duplicate(self, old_material):
        all_materials, _ = self.list_all_material_types()
        material_without_duplicate = []
        for material in all_materials['materialTypes']:
            if material['name'] != old_material:
                material_without_duplicate.append(material)
        return material_without_duplicate

    def is_article_enabled(self):
        response, _ = self.has_articles()
        return response['reponse'][0]['isAllowed']

    def is_dynamic_field_existing(self, field_name):
        response, _ = self.get_configuration()
        for field in response['fields']:
            if field.get('dynamicComponent'):
                if field_name in field['dynamicComponent']['fieldName']:
                    return True
        else:
            return False

    def get_dynamic_feilds(self, section=1):
        response, _ = self.get_configuration()
        dynamic_feilds = []
        for field in response['fields']:
            if field.get('dynamicComponent') and field.get('section') == section:
                dynamic_feilds.append(field['dynamicComponent']['fieldName'])
        return dynamic_feilds