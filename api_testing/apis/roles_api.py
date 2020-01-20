from api_testing.apis.base_api import BaseAPI
import json


class RolesAPI(BaseAPI):
    def get_all_roles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['roles_api']['list_all_roles'])
        _payload = {"sort_value": "id",
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

    def get_role_form_data(self, id=1):
        api = '{}{}{}/edit-view'.format(self.url, self.END_POINTS['roles_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['role']
        else:
            return False
    
    def archive_roles(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['roles_api']['archive_roles'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_roles(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['roles_api']['restore_roles'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='restore_success':
            return True
        else:
            return False
    
    def delete_archived_role(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['roles_api']['delete_role'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_role(self, id=1):
        if self.archive_roles(ids=[str(id)]):
            if self.delete_archived_role(id=id):
                return True
            else:
                self.restore_roles(ids=[str(id)])
                return False
        else:
            return False

    # this API call doesn't need kwargs as those are the only arguments sent 
    def create_role(self, role_name='', permissions=[]):

        """
        permession list can be obtained using this API call
        general_utilities_api.list_all_permissions()
        """
        request_body = {
            'name': role_name,
            'permissions': permissions
        }
        api = '{}{}'.format(self.url, self.END_POINTS['roles_api']['create_role']) 
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=request_body, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        
        if data['status'] == 1:
            return request_body
        else:
            return data['message']
