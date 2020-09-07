from api_testing.apis.base_api import BaseAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from ui_testing.pages.testunit_page import TstUnit
from api_testing.apis.base_api import api_factory
import random, json, os


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
        param id: order ID
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_suborder'], str(id) + '&deleted=0')
        return api, {}

    @api_factory('get')
    def get_suborder_of_archived_order(self, id=0):
        """
        param id: order ID
        deleted '0' for active orders and '1' for archived orders
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_suborder'], str(id) + '&deleted=1')
        return api, {}

    @api_factory('post')
    def create_new_order(self, **kwargs):
        """
        Create an order
        :param kwargs:
        :return: response, payload
        """
        order_no = self.get_auto_generated_order_no()[0]['id']
        testplan = random.choice(TestPlanAPI().get_completed_testplans(limit=1000))
        material_type = testplan['materialTypes'][0]
        material_type_id = GeneralUtilitiesAPI().get_material_id(material_type)
        testplan_form_data = TestPlanAPI()._get_testplan_form_data(id=testplan['id'])[0]
        article = testplan_form_data['testPlan']['selectedArticles'][0]['name']
        article_id = testplan_form_data['testPlan']['selectedArticles'][0]['id']
        if article == 'all':
            article, article_id = ArticleAPI().get_random_article_articleID()

        # modify_test_plan_ID
        testplan['id'] = testplan_form_data['testPlan']['testPlanEntity']['id']
        testunit = testplan_form_data['testPlan']['specifications'][0]

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
                "withArticle": True,
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
    def get_auto_generated_order_no(self, year_option="1"):
        """
        :param year_option:
        year_option = 1 : order no with year after (1668-2020)
        year_option = 0 : order no with year before (2020-1668)
        :return:
        """
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['get_auto_generated_number'])+year_option
        return api, {}

    @api_factory('put')
    def archive_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'delete_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['archive_main_order'],
                                                str(mainorder_id))
        return api, {}

    @api_factory('put')
    def restore_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'restore_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['restore_main_order'],
                                                str(mainorder_id))
        return api, {}

    @api_factory('delete')
    def delete_main_order(self, mainorder_id):
        """
        if success, response['message'] == 'delete_success'
        :param mainorder_id:
        :return: response, payload
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['delete_main_order'],
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
    def get_all_orders_json(self, **kwargs):
        orders_response, _ = self.get_all_orders(**kwargs)
        return orders_response['orders']

    def get_order_with_multiple_sub_orders(self):
        api, payload = self.get_all_orders(limit=100)
        all_orders = api['orders']
        for order in all_orders:
            suborder = self.get_suborder_by_order_id(id=order['orderId'])[0]['orders']
            if len(suborder) > 1:
                return order

    def get_order_with_field_name(self, field, no_of_field):
        """
        :param field: must be in this list ['article', 'materialType','analysis','testPlans','testUnit']
        :return: order, suborder, suborder_index
        """
        orders_data, payload = self.get_all_orders()
        orders = orders_data['orders']
        for order in orders:
            suborders_data, a = self.get_suborder_by_order_id(order['id'])
            suborders = suborders_data['orders']
            for i in range(0, len(suborders) - 1):
                if field in suborders[i].keys():
                    if suborders[i][field] and suborders[i][field] != "-" \
                            and len(suborders[i][field]) == int(no_of_field):
                        return order, suborders, i

    def get_order_with_testunit_testplans(self):
        """
        :return: order, suborder,
        """
        orders_data, payload = self.get_all_orders(limit=50)
        orders = orders_data['orders']
        for order in orders:
            suborders_data, a = self.get_suborder_by_order_id(order['id'])
            suborders = suborders_data['orders']
            for i in range(0, len(suborders) - 1):
                if suborders[i]['testPlans'] and suborders[i]['testUnit']:
                    return order, suborders

    def get_random_contact_in_order(self):
        """
        :return: contact name
        """
        orders_data, payload = self.get_all_orders(limit=50)
        orders = orders_data['orders']
        for order in orders:
            if order['company']:
                return order['company'][0]['name']

    def get_random_department_in_order(self):
        """
        :return: contact name
        """
        orders_data, payload = self.get_all_orders()
        orders = orders_data['orders']
        for order in orders:
            suborders_data, a = self.get_suborder_by_order_id(order['id'])
            suborders = suborders_data['orders']
            for i in range(0, len(suborders) - 1):
                if suborders[i]['departments']:
                    return suborders[i]['departments']

    def create_order_with_double_test_plans(self, only_test_plans=False):
        testplan1 = TestPlanAPI().create_completed_testplan_random_data()
        article = testplan1['selectedArticles'][0]['text']
        article_id = testplan1['selectedArticles'][0]['id']
        if article == 'all':
            article, article_id = ArticleAPI().get_random_article_articleID()
        material_type = testplan1['materialType'][0]

        tu_response1, tu_payload1 = TestUnitAPI().create_qualitative_testunit()
        testunit1 = TestUnitAPI().get_testunit_form_data(id=tu_response1['testUnit']['testUnitId'])[0]['testUnit']
        tu_response2, tu_payload2 = TestUnitAPI().create_qualitative_testunit()
        testunit2 = TestUnitAPI().get_testunit_form_data(id=tu_response2['testUnit']['testUnitId'])[0]['testUnit']
        if only_test_plans:
            testunit_list = []
        else:
            testunit_list = [testunit1, testunit2]
        formated_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit2)
        formatted_article = {'id': article_id, 'text': article}
        testplan2, _ = TestPlanAPI().create_testplan(testUnits=[formated_testunit],
                                                     selectedArticles=[formatted_article],
                                                     materialTypes=material_type)
        firsr_testPlan_data = TestPlanAPI()._get_testplan_form_data(id=testplan1['testPlan']['id'])
        testPlan1 = {
            'id': int(firsr_testPlan_data[0]['testPlan']['testPlanEntity']['id']),  # article_test_plan_id
            'testPlanName': firsr_testPlan_data[0]['testPlan']['testPlanEntity']['name'],
            'number': int(firsr_testPlan_data[0]['testPlan']['number']),
            'version': 1
        }
        second_testPlan_data = TestPlanAPI()._get_testplan_form_data(id=testplan2['testPlanDetails']['id'])
        testPlan2 = {
            'id': int(second_testPlan_data[0]['testPlan']['testPlanEntity']['id']),  # article_test_plan_id
            'testPlanName': second_testPlan_data[0]['testPlan']['testPlanEntity']['name'],
            'number': int(second_testPlan_data[0]['testPlan']['number']),
            'version': 1
        }
        testplan_list = [testPlan1, testPlan2]

        payload = {
            'testPlans': testplan_list,
            'testUnits': testunit_list,
            'materialType': material_type,
            'materialTypeId': material_type['id'],
            'article': {'id': article_id, 'text': article},
            'articleId': article_id
        }
        return self.create_new_order(**payload)

    def create_order_with_multiple_contacts(self):
        contacts = random.choices(ContactsAPI().get_contacts_with_department(), k=3)
        first_contact = contacts[0]
        second_contact = contacts[1]
        third_contact = contacts[2]
        payload = {
            'contact': [
                {"id": first_contact['id'],
                 "text": first_contact['name'],
                 'No': first_contact['companyNo']},
                {"id": second_contact['id'],
                 "text": second_contact['name'],
                 'No': second_contact['companyNo']},
                {"id": third_contact['id'],
                 "text": third_contact['name'],
                 'No': third_contact['companyNo']}
            ]

        }
        return self.create_new_order(**payload)

    def create_order_with_department(self):
        contact = random.choice(ContactsAPI().get_contacts_with_department())
        department_data = ContactsAPI().get_contact_form_data(contact['id'])[0]['contact']['departments'][0]
        payload = {
            'contact': [
                {"id": contact['id'],
                 "text": contact['name'],
                 'No': contact['companyNo']},
            ],
            'departments': [{"id": department_data['id'], "text": department_data['name'],
                             "group": contact['id'], "groupName": contact['name']}],
        }
        return self.create_new_order(**payload)

    def create_order_with_department_by_contact_id(self, contact_id):
        contact = ContactsAPI().get_contact_form_data(contact_id)[0]['contact']
        department_data = contact['departments'][0]
        payload = {
            'contact': [
                {"id": contact['id'],
                 "text": contact['name'],
                 'No': contact['companyNumber']},
            ],
            'departments': [{"id": department_data['id'], "text": department_data['name'],
                             "group": contact['id'], "groupName": contact['name']}],
        }
        return self.create_new_order(**payload)

    def create_order_with_test_units(self, no_of_test_units):
        test_units = []
        material_type = {
            'selectedMaterialTypes': [{
                'id': 1,
                'text': 'Raw Material'
            }]
        }
        for _ in range(no_of_test_units):
            res, payload = TestUnitAPI().create_qualitative_testunit(**material_type)
            res_form, pay_form = TestUnitAPI().get_testunit_form_data(res['testUnit']['testUnitId'])
            test_units.append({'id': res_form['testUnit']['id'],
                               'name': res_form['testUnit']['name']})
        payload = {
            'testPlans': [],
            'testUnits': test_units,
            'materialType': {"id": 1, "text": 'Raw Material'},
            'materialTypeId': 1
        }
        return self.create_new_order(**payload)

    def set_configuration(self):
        self.info('set order configuration')
        config_file = os.path.abspath('api_testing/config/order.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)

    def set_contact_configuration_to_number_only(self):
        self.info('set order configuration')
        config_file = os.path.abspath('api_testing/config/order_contact_number.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)