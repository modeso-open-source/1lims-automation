from api_testing.apis.base_api import BaseAPI


class GeneralUtilitiesAPI(BaseAPI):
    def list_all_permissions(self):
        api = '{}{}'.format(self.url, self.END_POINTS['components']['list_components']) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            permissions_list = []
            components = data['components']
            for component in components:
                permissions_list.append(self.map_component_to_permission(component=component))
                for item in component['items']:
                    permissions_list.append(self.map_component_to_permission(component=item))
            return permissions_list
        return []
    
    def list_all_material_types(self):
        api = '{}{}'.format(self.url, self.END_POINTS['materialTypes']['list_material_types']) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['materialTypes']
        return []

    def map_component_to_permission(self, component):
        return {
            'id': component['id'],
            'name': component['name'],
            'view': False,
            'modify': False
        }