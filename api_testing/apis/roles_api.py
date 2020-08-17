from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


class RolesAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_roles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['roles_api']['list_all_roles'])
        _payload = {"sort_value": "id",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def get_role_form_data(self, id=1):
        """
        if success, response['role']
        :param id:
        :return:
        """
        api = '{}{}{}/edit-view'.format(self.url, self.END_POINTS['roles_api']['form_data'], str(id)) 
        return api, {}

    @api_factory('put')
    def archive_roles(self, ids=['1']):
        """
        if success, response['message'] == 'delete_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['roles_api']['archive_roles'], ','.join(ids)) 
        return api, {}

    @api_factory('put')
    def restore_roles(self, ids=['1']):
        """
        if success, response['message']=='restore_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['roles_api']['restore_roles'], ','.join(ids)) 
        return api, {}

    @api_factory('delete')
    def delete_archived_role(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['roles_api']['delete_role'], str(id)) 
        return api, {}

    @api_factory('post')
    def create_role(self, role_name='', permissions=[]):

        """
        permession list can be obtained using this API call
        general_utilities_api.list_all_permissions()
        """
        _payload = {
            'name': role_name,
            'permissions': permissions
        }
        api = '{}{}'.format(self.url, self.END_POINTS['roles_api']['create_role']) 
        return api, _payload


class RolesAPI(RolesAPIFactory):
    def delete_active_role(self, id=1):
        if self.archive_roles(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_role(id=id)[0]['meessage'] == 'hard_delete_success':
                return True
            else:
                self.restore_roles(ids=[str(id)])
                return False
        else:
            return False

    def get_random_role(self):
        response, payload = RolesAPI().get_all_roles()
        roles = response['roles']
        editable_roles = [role for role in roles if role['name'] not in ['Admin', 'Contact']]
        return editable_roles
