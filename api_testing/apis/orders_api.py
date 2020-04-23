from api_testing.apis.base_api import BaseAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.base_api import api_factory
import random


class OrdersAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_orders(self, **kwargs):
        """
        :param kwargs:
        :return: response, payload
        """
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['list_all_orders'])
        _payload = {"sort_value": "createdAt",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def get_order_by_id(self, id=1, **kwargs):
        """

        :param id: order ID
        :param kwargs:
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_order_by_id'], str(id))
        return api, {}

    @api_factory('get')
    def get_suborder_by_order_id(self, id=0):
        """
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_suborder'], str(id) + '&deleted=0')
        return api, {}

    @api_factory('post')
    def create_new_order(self, **kwargs):
        """
        Create an order
        :param kwargs:
        :return: response, payload
        """

        order_no = self.get_auto_generated_order_no()[0]['id']
        if 'testplan' not in kwargs.keys():
            testplan = random.choice(TestPlanAPI().get_completed_testplans())
            material_type = testplan['materialType']
            material_type_id = GeneralUtilitiesAPI().get_material_id(material_type)
            article = testplan['article'][0]
            article_api = ArticleAPI()
            if article == "all":
                res, _ = article_api.get_all_articles(limit=20)
            else:
                res, _ = article_api.quick_search_article(name=article)
            article_id = res['articles'][0]['id']
            testunit = random.choice(TestUnitAPI().list_testunit_by_name_and_material_type(
                materialtype_id=material_type_id)[0]['testUnits'])

        test_date = self.get_current_date()
        shipment_date = self.get_current_date()
        current_year = self.get_current_year()
        contacts = random.choice(ContactsAPI().get_all_contacts()[0]['contacts'])
        _payload = [
            {
                'orderNo': int(order_no),
                'contact': [
                    {"id": contacts['id'],
                     "text": contacts['name'],
                     'No': contacts['companyNo']}
                ],
                'deletedTestPlans': [],
                'deletedAnalysisIds': [],
                'dynamicFieldsValues': [],
                'analysisNo': [],
                'selectedDepartments': [],
                'orderType': {
                    'id': 1,
                    'text': 'New Order'
                },
                'departments': [],
                'attachments': [],
                'testPlans': [testplan],
                'selectedTestPlans': [],
                'testUnits': [testunit],
                'selectedTestUnits': [],
                'materialType': {"id": material_type_id, "text": material_type},
                'materialTypeId': material_type_id,
                'article': {'id': article_id,
                            'text': article},
                'articleId': article_id,
                'shipmentDate': shipment_date,
                'testDate': test_date,
                'year': current_year,
                'yearOption': 1
            }]
        payload = self.update_payload(_payload, **kwargs)
        payload = self._format_payload(payload)
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['create_new_order'])
        return api, payload

    @api_factory('get')
    def get_auto_generated_order_no(self):
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['get_auto_generated_number'])
        return api, {}

    @api_factory('put')
    def archive_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'delete_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}/archive/mainOrder'.format(self.url, self.END_POINTS['orders_api']['archive_testunits'],
                                                str(mainorder_id))
        return api, {}

    @api_factory('put')
    def restore_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'restore_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}/restore/mainOrder'.format(self.url, self.END_POINTS['orders_api']['restore_main_order'],
                                                str(mainorder_id))
        return api, {}

    @api_factory('delete')
    def delete_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'delete_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}/delete/mainOrder'.format(self.url, self.END_POINTS['orders_api']['delete_main_order'],
                                               str(mainorder_id))
        return api, {}

    @api_factory('put')
    def archive_sub_order(self, suborder_id):
        """
        if success, response['message'] == 'delete_success'
        :param suborder_id:
        :return: response, payload
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['orders_api']['archive_suborder'], str(suborder_id))
        return api, {}

    @api_factory('put')
    def restore_sub_order(self, suborder_id):
        """
        If success, response['message'] == 'restore_success'
        :param suborder_id:
        :return: response, payload
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['orders_api']['restore_suborder'], str(suborder_id))
        return api, {}

    @api_factory('delete')
    def delete_sub_order(self, suborder_id):
        """
        If success, response['message'] == 'delete_success'
        :param suborder_id:
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['delete_suborder'], str(suborder_id))
        return api, {}

    @staticmethod
    def _format_payload(payload):
        payload = payload[0]
        if payload['testPlans']:
            selected_testplan_arr = []
            for testplan in payload['testPlans']:
                selected_testplan_arr.append({
                    'id': int(testplan['id']),
                    'name': testplan['testPlanName'],
                    'version': testplan['version']
                })
            payload['selectedTestPlans'] = selected_testplan_arr
            payload['testPlans'] = selected_testplan_arr
        else:
            payload['testPlans'] = []
            payload['selectedTestPlans'] = []

        if 'testUnits' in payload:
            selected_testunits_arr = []
            for testunit in payload['testUnits']:
                selected_testunits_arr.append({
                    'id': int(testunit['id']),
                    'name': testunit['name'],
                    'new': True
                })
                payload['selectedTestUnits'] = selected_testunits_arr
                payload['testUnits'] = selected_testunits_arr
        else:
            payload['testUnits'] = []
            payload['selectedTestUnits'] = []

        if 'shipmentDate' in payload and payload['shipmentDate'] != '':
            shipment_date_arr = payload['shipmentDate'].split('-')
            payload['shipmentDatedateOption'] = {
                'year': shipment_date_arr[0],
                'month': shipment_date_arr[1],
                'day': shipment_date_arr[2]
            }

        test_date_arr = payload['testDate'].split('-')
        payload['testDatedateOption'] = {
            'year': test_date_arr[0],
            'month': test_date_arr[1],
            'day': test_date_arr[2]
        }

        if payload['yearOption'] == 1:
            payload['orderNoWithYear'] = "{}-{}".format((payload['orderNo']), payload['year'])
        elif payload['yearOption'] == 2:
            payload['orderNoWithYear'] = "{}-{}".format(payload['year'], payload['orderNo'])

        return [payload]


class OrdersAPI(OrdersAPIFactory):
    def get_order_with_multiple_sub_orders(self):
        api, payload = self.get_all_orders(limit=100)
        all_orders = api['orders']
        for order in all_orders:
            suborder = self.get_suborder_by_order_id(id=order['orderId'])[0]['orders']
            if len(suborder) > 1:
                return order

