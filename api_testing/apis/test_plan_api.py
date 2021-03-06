from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from ui_testing.pages.testunit_page import TstUnit
import random, json, os


class TestPlanAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_test_plans(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_all_test_plans'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": '{"quickSearch": ""}',
                    "deleted": "0"}
        # api = f"{self.url}/api/testPlans?sort_value=number&limit=100&start=0&sort_order=DESC&filter=%7B%22quickSearch%22:%22%22%7D&deleted=0"
        # _payload = {}
        return api, _payload

    @api_factory('get')
    def _get_testunits_in_testplan(self, id):
        """
        If success, testunits = response['testPlan']['specifications']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['get_testunits_in_testplan'], id)
        return api, {}

    @api_factory('get')
    def get_testplan_testunits(self, id=1):
        """
        if success, response['specifications']
        :param id:
        :return:
        """
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['list_testplan_testunits'])
        _payload = {"sort_value": "id",
                    "limit": 100,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": '{"id": ' + str(id) + '}'
                    }
        return api, _payload

    @api_factory('get')
    def _get_testplan_form_data(self, id=1):
        """
        if success, response['testPlan']
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['form_data'], str(id))
        return api, {}

    @api_factory('put')
    def archive_testplans(self, ids=['1']):
        """
        if success, response['message'] == 'delete_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_plan_api']['archive_testplans'], ','.join(ids))
        return api, {}

    @api_factory('put')
    def restore_testplans(self, ids=['1']):
        """
        if success, response['message']=='restore_success'
        :param ids:
        :return:
        """
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_plan_api']['restore_testplans'], ','.join(ids))
        return api, {}

    @api_factory('delete')
    def delete_archived_testplan(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_plan_api']['delete_testplan'], str(id))
        return api, {}

    @api_factory('post')
    def create_testplan(self, **kwargs):
        """
        NOTE: calling this api without adding testunits, will create an in progress testplan, to create a complete testplan
        you will need to pass parameter testunits[testunit_object], and this object is can be formated by the following steps,
        testunit = self.test_unit_api.get_testunit_form_data(id=#testunit_id)
        formated_testunit = self.test_unit_page.map_testunit_to_testplan_format(testunit=testunit)
        self.test_plan_api.create_testplan(testunits=[formated_testunit])
        param: testplan: {
            'id': testplan id, 'new' in case of new testplan name,
            'text': testplan name text
        }
        param: 'number': testplan number
        param: 'selectedArticles':  denotes articles that support this testplan, all by default[{
            'id': article id,
            'text': article name
        }]
        param: materialType: testplan material type, raw material by default{
            'id': material type id,
            'text': material type text
        }
        param testUnits: testunits in this testplan, if empty, it will be created as in progress testplan, else
        put array of testunits by the following way
        using testunit id, select testunit form data through api call: test_unit_api.get_testunit_form_data(id=#testunit_id)
        and then use the return of this mapping function test_unit_page.map_testunit_to_testplan_format(testunit=formdata_testunit) to add it to the testunits array
        """
        api = '{}{}'.format(self.url, self.END_POINTS['test_plan_api']['create_testplan'])
        testplan_name = self.generate_random_string()
        _payload = {
            'number': self.generate_random_number(),
            'testPlan': {
                'id': 'new',
                'text': testplan_name
            },
            'selectedTestPlan': {
                'id': 'new',
                'text': testplan_name
            },
            'selectedArticles': [{
                'id': -1,
                'text': 'All'
            }],
            'materialType': [{
                'id': 1,
                'text': 'Raw Material'
            }],
            'attachments': '[]',
            'selectedTestUnits': [],
            'materialTypeId': [1],
            'dynamicFieldsValues': [],
            'testUnits': []
        }
        payload = self.update_payload(_payload, **kwargs)
        if 'testPlan' in kwargs:
            payload['selectedTestPlan'] = [kwargs['testPlan']['text']]
        if 'materialType' in kwargs:
            payload['materialType'] = kwargs['materialType']
            payload['materialTypeId'] = [kwargs['materialType'][0]['id']]

        return api, payload

    @api_factory('get')
    def list_testunit_by_name_and_material_type(self, materialtype_id, name='', negelectIsDeleted=0,
                                                searchableValue=''):
        """
        if success, response['testUnits]
        :param materialtype_id:
        :param name:
        :param negelectIsDeleted:
        :param searchableValue:
        :return:
        """
        api = '{}{}{}?name={}&negelectIsDeleted={}&searchableValue={}'.format(self.url,
                                                                              self.END_POINTS['test_unit_api'][
                                                                                  'list_testunit_by_name_and_materialtype'],
                                                                              materialtype_id, name, negelectIsDeleted,
                                                                              searchableValue)
        return api, {}


class TestPlanAPI(TestPlanAPIFactory):
    def get_all_test_plans_json(self, **kwargs):
        testplans_response, _ = self.get_all_test_plans(**kwargs)
        return testplans_response['testPlans']

    def get_completed_testplans(self, **kwargs):
        response, _ = self.get_all_test_plans(**kwargs)
        all_test_plans = response['testPlans']
        completed_test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == 'Completed']
        return completed_test_plans

    def get_inprogress_testplans(self, **kwargs):
        response, _ = self.get_all_test_plans(**kwargs)
        all_test_plans = response['testPlans']
        inprogress_test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == 'InProgress']
        return inprogress_test_plans

    def get_testplans_with_status(self, status):
        response, _ = self.get_all_test_plans()
        all_test_plans = response['testPlans']
        test_plans = [test_plan for test_plan in all_test_plans if test_plan['status'] == status]
        return test_plans

    def get_testunits_in_testplan(self, id=1):
        response, _ = self._get_testunits_in_testplan(id)
        return response['testPlan']['specifications']

    def get_testunits_names_in_testplans(self, ids=[1]):
        test_units = []
        for id in ids:
            response, _ = self._get_testunits_in_testplan(id)
            tus_data = response['testPlan']['specifications']
            names = [tu['name'] for tu in tus_data]
            test_units.extend(names)
        return test_units

    def get_testplan_with_quicksearch(self, quickSearchText):
        filter_text = f'{{"quickSearch":"{quickSearchText}","columns":["number","name","materialType","articleName","articleNo","modifiedAt","modifiedBy","status","version","createdAt"]}}'
        response, _ = self.get_all_test_plans(filter=filter_text, start=0)
        return response['testPlans']

    def get_testplan_with_filter(self, filter_option, filter_text):
        filter_text = '{"quickSearch": "", "' + filter_option + '":"' + filter_text + '","columns":["number","name"]}'
        response, _ = self.get_all_test_plans(filter=filter_text, start=0)
        return response['testPlans']

    def get_testplan_form_data(self, id=1):
        response, _ = self._get_testplan_form_data(id)
        return response['testPlan']

    def delete_active_testplan(self, id=1):
        if self.archive_testplans(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_testplan(id=id)[0]['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_testplans(ids=[str(id)])
                return False
        else:
            return False

    def get_completed_testplans_with_material_and_same_article(self, material_type, article, articleNo):
        all_test_plans = self.get_completed_testplans(limit=1000)
        completed_test_plans = [test_plan for test_plan in all_test_plans if
                                test_plan['materialTypes'] == material_type]
        test_plan_same_article = []
        for testplan in completed_test_plans:
            if testplan['article'][0] in [article, 'all'] and testplan['articleNo'][0] in [articleNo, 'all']:
                test_plan_same_article.append(testplan)
        return test_plan_same_article

    def create_completed_testplan(self, material_type, formatted_article):
        material_type_id = GeneralUtilitiesAPI().get_material_id(material_type)
        formatted_material = {'id': material_type_id, 'text': material_type}
        tu_response, tu_payload = TestUnitAPI().create_qualitative_testunit()
        testunit_data = TestUnitAPI().get_testunit_form_data(
            id=tu_response['testUnit']['testUnitId'])[0]['testUnit']
        formated_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit_data)
        testplan, payload = self.create_testplan(testUnits=[formated_testunit],
                                                 selectedArticles=[formatted_article],
                                                 materialType=[formatted_material],
                                                 material_type_id=material_type_id)

        if testplan['message'] == 'operation_success':
            return self.get_testplan_form_data(id=int(testplan['testPlanDetails']['id']))
        else:
            self.info(testplan)

    def get_order_valid_testplan_and_test_unit(self, material_type, article_id, article, used_test_plan,
                                               used_test_unit):
        article_no = ArticleAPI().get_article_form_data(id=article_id)[0]['article']['No']
        self.info("get new completed test plan with article {} No: {} and material_type {}".format(
            article, article_no, material_type))
        completed_test_plan_list = self.get_completed_testplans_with_material_and_same_article(
            material_type=material_type, article=article, articleNo=article_no)
        completed_test_plans = [testplan for testplan in completed_test_plan_list if
                                testplan['testPlanEntity']['name'] not in used_test_plan]
        if completed_test_plans:
            new_test_plan_data = random.choice(completed_test_plans)
            new_test_plan = new_test_plan_data['testPlanEntity']['name']
            new_test_unit = new_test_plan_data['specifications'][0]['name']
            self.info("completed test plan found with name {} and test unit {}".format(new_test_plan, new_test_unit))
        else:
            self.info("There is no completed test plan so create it ")
            formatted_article = {'id': article_id, 'text': article}
            test_plan = self.create_completed_testplan(material_type=material_type, formatted_article=formatted_article)
            new_test_plan = test_plan['testPlanEntity']['name']
            new_test_unit = test_plan['specifications'][0]['name']
            self.info("completed test plan created with name {} and test unit {}".format(new_test_plan, new_test_unit))

        if new_test_unit in used_test_unit:
            api, payload = TestUnitAPI().create_quantitative_testunit()
            if api['status'] == 1:
                new_test_unit = payload['name']

        return new_test_plan, new_test_unit

    def get_testunits_in_testplan_by_No(self, no):
        test_plan_id = self.get_testplan_with_filter(filter_option='number', filter_text=str(no))[0]['id']
        test_units = self.get_testunits_in_testplan(test_plan_id)
        test_units_names = [testunit['name'] for testunit in test_units]
        return test_units_names

    def get_suborder_data_with_different_material_type(self, material_type):
        new_material = random.choice(
            GeneralUtilitiesAPI().get_formatted_material_types_without_duplicate(material_type))
        formatted_material = {'id': new_material['id'], 'text': new_material['name']}
        formatted_article = ArticleAPI().get_formatted_article_with_formatted_material_type(
            material_type=formatted_material)
        test_plan_data = self.create_completed_testplan(material_type=new_material['name'],
                                                        formatted_article=formatted_article)
        created_data = {'test_plan': test_plan_data['testPlanEntity']['name'],
                        'test_unit': test_plan_data['specifications'][0]['name'],
                        'material_type': new_material['name'],
                        'article': formatted_article['name']}
        return created_data

    def create_testplan_from_test_unit_id(self, test_unit_id):
        testunit_data = TestUnitAPI().get_testunit_form_data(id=test_unit_id)[0]['testUnit']
        if testunit_data['materialTypesObject'][0]['name'] == 'All':
            response, _ = GeneralUtilitiesAPI().list_all_material_types()
            _formatted_material = random.choice(response['materialTypes'])
        else:
            _formatted_material = testunit_data['materialTypesObject'][0]

        formatted_material = {'id': _formatted_material['id'], 'text': _formatted_material['name']}

        # tu_response, tu_payload = TestUnitAPI().create_qualitative_testunit()
        testunit_data = TestUnitAPI().get_testunit_form_data(
            id=test_unit_id)[0]['testUnit']
        formated_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit_data)
        formatted_article = ArticleAPI().get_formatted_article_with_formatted_material_type(formatted_material)
        testplan, payload = self.create_testplan(testUnits=[formated_testunit],
                                                 selectedArticles=[formatted_article],
                                                 materialType=[formatted_material],
                                                 materialTypeId=[formatted_material['id']])

        if testplan['message'] == 'operation_success':
            return self.get_testplan_form_data(id=payload['number'])
        else:
            self.info(testplan)

    def create_testplan_with_article_not_all(self):
        response, _ = GeneralUtilitiesAPI().list_all_material_types()
        formatted_material = random.choice(response['materialTypes'])

        formatted_article = ArticleAPI().get_formatted_article_with_formatted_material_type(formatted_material)
        testplan, payload = self.create_testplan(selectedArticles=[formatted_article],
                                                 materialType=[formatted_material])
        if testplan['message'] == 'operation_success':
            return (self.get_testplan_form_data(id=payload['number']))
        else:
            raise Exception(f'cant create the test plan with payload {payload}')

    def create_completed_testplan_random_data(self, no_testunits=1):
        random_article = random.choice(ArticleAPI().get_all_articles_json())
        formatted_article = {'id': random_article['id'], 'text': random_article['name']}
        material_type_id = GeneralUtilitiesAPI().get_material_id(random_article['materialType'])
        formatted_material = {'id': material_type_id, 'text': random_article['materialType']}
        # creates test unit with values in it
        formatted_testunits = []
        for testunit in range(no_testunits):
            tu_response, _ = TestUnitAPI().create_quantitative_testunit(selectedMaterialTypes=[formatted_material])
            testunit_data = TestUnitAPI().get_testunit_form_data(
                id=tu_response['testUnit']['testUnitId'])[0]['testUnit']
            formatted_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit_data)
            formatted_testunits.append(formatted_testunit)

        testplan, payload = self.create_testplan(testUnits=formatted_testunits,
                                                 selectedArticles=[formatted_article],
                                                 materialType=[formatted_material],
                                                 materialTypeId=[material_type_id])

        if testplan['message'] == 'operation_success':
            payload['testPlan']['id'] = testplan['testPlanDetails']['testPlanId']
            payload['selectedTestPlan']['id'] = testplan['testPlanDetails']['testPlanId']
            return payload
        else:
            return None

    def get_testplans_matches_material_types(self, testplans, material_type):
        testplan_materials = []
        testplans_materials = []
        for testplan in testplans:
            testplan_info = self.get_testplan_with_quicksearch(quickSearchText=testplan)
            if testplan_info is not None:
                for tp in testplan_info:
                    if tp['testPlanName'] == testplan:
                        for material in tp['materialTypes']:
                            testplan_materials.append(material)
            if len(testplan_materials) == 1:
                testplans_materials.extend(testplan_materials)
            elif len(testplan_materials) > 1:
                if material_type in testplan_materials:
                    testplans_materials.append(material_type)

        return testplan_materials

    def create_double_completed_testplan_same_name_diff_material(self, **kwargs):
        self.info("create completed test plan with random data")
        testplan1 = self.create_completed_testplan_random_data()
        test_plan_name_dict = {'id': 'new', 'text': testplan1['testPlan']['text']}
        new_material = random.choice(GeneralUtilitiesAPI().get_material_types_without_duplicate(
            testplan1['materialType'][0]['text']))
        new_material_id = GeneralUtilitiesAPI().get_material_id(new_material)
        formatted_material = {'id': new_material_id, 'text': new_material}
        tu_response, _ = TestUnitAPI().create_qualitative_testunit(selectedMaterialTypes=[formatted_material])
        testunit_data = TestUnitAPI().get_testunit_form_data(id=tu_response['testUnit']['testUnitId'])[0]['testUnit']
        formated_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit_data)
        self.info("create completed test plan with same name {} and new material {}".format(
            testplan1['testPlan']['text'], new_material))
        formatted_article = ArticleAPI().get_formatted_article_with_formatted_material_type(
            material_type=formatted_material)
        response, testplan2 = self.create_testplan(selectedTestPlan=test_plan_name_dict,
                                                   testPlan=test_plan_name_dict,
                                                   testUnits=[formated_testunit],
                                                   selectedArticles=[formatted_article],
                                                   materialType=[formatted_material],
                                                   materialTypeId=[new_material_id])

        if response['message'] == 'name_already_exist':
            testplan2['testPlan']['id'] = response['testPlanDetails']['testPlanId']
            testplan2['selectedTestPlan']['id'] = response['testPlanDetails']['testPlanId']
            return [testplan1, testplan2]
        else:
            raise Exception(f'cant create the test plan with payload {testplan2}')

    def set_configuration(self):
        self.info('set test Plan configuration')
        config_file = os.path.abspath('api_testing/config/test_plan.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)

    def create_multiple_test_plan_with_same_article(self, no_of_testplans=2):
        materialType = {"id": 1, "text": 'Raw Material'}
        article_data = ArticleAPI().get_formatted_article_with_formatted_material_type(materialType)
        article_name = article_data['name']
        formatted_article = {'id': article_data['id'], 'text': article_name}
        formatted_material_type = {'id': 1, 'text': 'Raw Material'}
        testPlans = []
        test_units_in_test_plan = []
        for _ in range(no_of_testplans):
            tp = TestPlanAPI().create_completed_testplan(
                material_type='Raw Material', formatted_article=formatted_article)
            testPlans.append({'id': int(tp['id']), 'name': tp['testPlanEntity']['name'], 'version': 1})
            test_units_in_test_plan.append(tp['specifications'][0]['name'])

        created_data = {'material_type': formatted_material_type,
                        'article': formatted_article,
                        'testPlans': testPlans,
                        'test_units': test_units_in_test_plan}
        return created_data

    def create_testplan_with_multiple_materials(self, no_materials=3):
        all_material_types = GeneralUtilitiesAPI().list_all_material_types()[0]['materialTypes']
        formatted_materials = random.sample(all_material_types, no_materials)
        material_type_ids = [material['id'] for material in formatted_materials]
        selected_material_types = [material['name'] for material in formatted_materials]
        tu_response, _ = TestUnitAPI().create_quantitative_testunit(selectedMaterialTypes=formatted_materials[0])
        testunit_data = TestUnitAPI().get_testunit_form_data(id=tu_response['testUnit']['testUnitId'])[0]['testUnit']
        formatted_testunit = TstUnit().map_testunit_to_testplan_format(testunit=testunit_data)
        testplan = self.create_testplan(testUnits=[formatted_testunit], materialType=formatted_materials,
                                        materialTypeId=material_type_ids)
        return testplan[1]['testPlan']['text'], selected_material_types
