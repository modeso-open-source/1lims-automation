from api_testing.apis.base_api import BaseAPI
import json

class UsersAPI(BaseAPI):
    def create_new_user(self, user_name, email, password, **kwargs):
        null = None
        true = True
        false = False
        api = '{}{}'.format(self.url, self.END_POINTS['users_api']['list_all_users'])
        body = {
            "username": user_name,
            "email": email,
            "role": {
                "id": 1,
                "text": "Admin"
            },
            "supplier": null,
            "supplierId": null,
            "password": password,
            "confirmPassword": password,
            "roleId": 1,
            "roleChanged": true,
            "hasOwnPermissions": false
        }
        json.dumps(body)
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=body, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response