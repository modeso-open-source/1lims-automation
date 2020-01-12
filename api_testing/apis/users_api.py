from api_testing.apis.base_api import BaseAPI
import json

class UsersAPI(BaseAPI):
    def create_new_user(self, user_name, email, password, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['users_api']['list_all_users'])
        body = {
            "username": user_name,
            "email": email,
            "role": {
                "id": 1,
                "text": "Admin"
            },
            "supplier": None,
            "supplierId": None,
            "password": password,
            "confirmPassword": password,
            "roleId": 1,
            "roleChanged": True,
            "hasOwnPermissions": True
        }
        json.dumps(body)
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=body, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_all_users(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['users_api']['list_all_users'])
        _payload = {"sort_value": "userId",
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

    def get_user_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['users_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['user']
        else:
            return False
    
    def archive_users(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['users_api']['archive_users'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_users(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['users_api']['restore_users'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='restore_success':
            return True
        else:
            return False
    
    def delete_archived_user(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['users_api']['delete_user'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_user(self, id=1):
        if self.archive_users(ids=[str(id)]):
            if self.delete_archived_user(id=id):
                return True
            else:
                self.restore_users(ids=[id])
                return False
        else:
            return False
