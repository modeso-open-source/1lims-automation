from testconfig import config
import requests


class BaseAPI:
    def __init__(self):
        self.url = config['site']['url']
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
        response = self.session.post(api, json=data, header=header, verify=False)
        self.header['Authorization'] = 'Bearer {}'.format(response.json()['data']['sessionId'])

    @staticmethod
    def update_data(data, **kwargs):
        for key in kwargs:
            if key in data.keys():
                data[key] = kwargs[key]
            else:
                data[key] = kwargs[key]
        return data
