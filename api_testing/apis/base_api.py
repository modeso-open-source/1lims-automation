from testconfig import config
from api_testing.end_points import end_points
from uuid import uuid4
from random import randint
import requests
from loguru import logger
from datetime import datetime


class BaseAPI:
    END_POINTS = end_points
    requests.packages.urllib3.disable_warnings()

    AUTHORIZATION = None
    AUTHORIZATION_RESPONSE = None
    LOGGER = logger

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.url = config['site']['url']
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.username = config['site']['username']
        self.password = config['site']['password']

        self.session = requests.Session()
        self.headers = {'Content-Type': "application/json", 'Authorization': BaseAPI.AUTHORIZATION,
                        'Connection': "keep-alive",
                        'cache-control': "no-cache"}
        self._get_authorized_session()

    def _get_authorized_session(self, username=None, password=None, reset_token=False):
        username = username or self.username
        password = password or self.password
        if reset_token == True:
            BaseAPI.AUTHORIZATION = None
            self.headers['Authorization'] = None

        if not BaseAPI.AUTHORIZATION:
            self.info('Get authorized api session.')
            api = self.url + "/api/auth"
            header = {'Content-Type': "application/json", 'Authorization': "Bearer", 'Connection': "keep-alive",
                      'cache-control': "no-cache"}
            data = {'username': username, 'password': password}
            response = self.session.post(api, json=data, headers=header, verify=False)
            BaseAPI.AUTHORIZATION_RESPONSE = response.json()['data']
            BaseAPI.AUTHORIZATION = 'Bearer {}'.format(response.json()['data']['sessionId'])
            self.info('session ID : {} .....'.format(response.json()['data']['sessionId'][:10]))

        self.headers['Authorization'] = BaseAPI.AUTHORIZATION
        return BaseAPI.AUTHORIZATION

    @staticmethod
    def _update_payload(payload, **kwargs):
        for key in kwargs:
            if key in payload.keys():
                payload[key] = kwargs[key]
            else:
                payload[key] = kwargs[key]
        return payload

    @staticmethod
    def update_payload(payload, **kwargs):
        if type(payload) == list:
            return [BaseAPI._update_payload(payload[0], **kwargs)]
        return BaseAPI._update_payload(payload, **kwargs)

    @staticmethod
    def info(message):
        BaseAPI.LOGGER.info(message)

    @staticmethod
    def generate_random_string():
        return str(uuid4()).replace("-", "")[:10]

    @staticmethod
    def generate_random_number(lower=1, upper=100000):
        return randint(lower, upper)

    @staticmethod
    def get_current_date():
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def get_current_year():
        return str(datetime.now().year)


def api_factory(method):
    if method not in ['get', 'post', 'put', 'delete']:
        raise Exception("{} should be in ['get', 'post', 'put', 'delete']".format(method))

    def api_request(func):
        base_api = BaseAPI()

        def wrapper(*args, **kwargs):
            api, _payload = func(*args, **kwargs)
            payload = base_api.update_payload(_payload, **kwargs)
            base_api.info('GET : {}'.format(api))
            if method in ["post"]:
                response_json = base_api.session.post(api, json=payload, headers=base_api.headers,
                                                      verify=False).json()
            else:
                response_json = base_api.session.__getattribute__(method)(api, params=payload, headers=base_api.headers,
                                                                          verify=False).json()
            base_api.info('Status code: {}'.format(response_json['status']))
            return response_json, payload

        return wrapper

    return api_request


