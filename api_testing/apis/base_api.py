from testconfig import config
from api_testing.end_points import end_points
import requests


class BaseAPI:
    END_POINTS = end_points

    def __init__(self):
        self.url = config['site']['url']
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.username = config['site']['username']
        self.password = config['site']['password']

        self.session = requests.Session()
        self.header = {'Content-Type': "application/json", 'Authorization': "Bearer", 'Connection': "keep-alive", 'cache-control': "no-cache"}
        self._get_authorized_session()

    def _get_authorized_session(self):
        api = self.url + "/api/auth"
        header = {'Content-Type': "application/json", 'Authorization': "Bearer", 'Connection': "keep-alive",
                  'cache-control': "no-cache"}
        data = {'username': self.username, 'password': self.password}
        response = self.session.post(api, json=data, headers=header, verify=False)
        import ipdb; ipdb.set_trace()
        self.header['Authorization'] = 'Bearer {}'.format(response.json()['data']['sessionId'])

    @staticmethod
    def update_payload(payload, **kwargs):
        for key in kwargs:
            if key in payload.keys():
                payload[key] = kwargs[key]
            else:
                payload[key] = kwargs[key]
        return payload
