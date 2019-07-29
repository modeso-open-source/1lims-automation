from testconfig import config
from api_testing.end_points import end_points
import requests
from loguru import logger


class BaseAPI:
    END_POINTS = end_points
    requests.packages.urllib3.disable_warnings()

    LOGGER = logger

    def __init__(self):
        self.url = config['site']['url']
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.username = config['site']['username']
        self.password = config['site']['password']

        self.session = requests.Session()
        self.headers = {'Content-Type': "application/json", 'Authorization': "Bearer", 'Connection': "keep-alive", 'cache-control': "no-cache"}
        self._get_authorized_session()

    def _get_authorized_session(self):
        self.info('Get authorized api session.')
        api = self.url + "/api/auth"
        header = {'Content-Type': "application/json", 'Authorization': "Bearer", 'Connection': "keep-alive",
                  'cache-control': "no-cache"}
        data = {'username': self.username, 'password': self.password}
        response = self.session.post(api, json=data, headers=header, verify=False)
        self.headers['Authorization'] = 'Bearer {}'.format(response.json()['data']['sessionId'])
        self.info('session ID : {}'.format(response.json()['data']['sessionId']))

    @staticmethod
    def update_payload(payload, **kwargs):
        for key in kwargs:
            if key in payload.keys():
                payload[key] = kwargs[key]
            else:
                payload[key] = kwargs[key]
        return payload

    @staticmethod
    def info(message):
        BaseAPI.LOGGER.info(message)
