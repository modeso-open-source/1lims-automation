from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


class UsersAPIFactory(BaseAPI):
    @api_factory('post')
    def create_new_user(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['users_api']['list_all_users'])
        password = self.generate_random_string()
        _payload = {
            'username': self.generate_random_string(),
            'email': self.generate_random_string()+"@gmial.com",
            'role': {
                'id': 1,
                'text': 'Admin'
            },
            'password': password,
            'confirmPassword': password,
            'roleId': 1,
            'roleChanged': True,
            'hasOwnPermissions': False
        }
        return api, _payload

    @api_factory('get')
    def get_all_users(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['users_api']['list_all_users'])
        _payload = {"sort_value": "userId",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def get_user_form_data(self, id=1):
        """
        If success, response['user']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['users_api']['form_data'], str(id)) 
        return api, {}

    @api_factory('put')
    def archive_users(self, ids=['1']):
        """"
        if success, response['message'] == 'delete_success'
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['users_api']['archive_users'], ','.join(ids)) 
        return api, {}

    @api_factory('put')
    def restore_users(self, ids=['1']):
        """
        if success, response['message']=='restore_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['users_api']['restore_users'], ','.join(ids)) 
        return api, {}

    @api_factory('delete')
    def delete_archived_user(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['users_api']['delete_user'], str(id)) 
        return api, {}


class UsersAPI(UsersAPIFactory):
    def delete_active_user(self, id=1):
        if self.archive_users(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_user(id=id)[0]['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_users(ids=[str(id)])
                return False
        else:
            return False
