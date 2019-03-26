import requests
from api_testing.onelims_api.base_api import BaseAPI


class AccessToken(BaseAPI):
    def __init__(self):
        super().__init__()
        self.end_point = "/api/auth"
        self.api = self.base_url + self.end_point

    def acuire_access_token(self):
        response = requests.post(url=self.api, headers=self.headers, verify=False)
        return response

    def revoke_access_token(self):
        response = requests.get(url=self.api, headers=self.headers, verify=False)
        return response
   