from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
import random, json, os


class ArticleAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_articles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['list_all_articles'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def get_article_form_data(self, id=1, **kwargs):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['form_data'], str(id))
        _payload = {}
        return api, _payload

    @api_factory('put')
    def archive_articles(self, ids=['1'], **kwargs):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['article_api']['archive_articles'], ','.join(ids))
        _payload = {}
        return api, _payload

    @api_factory('put')
    def restore_articles(self, ids=['1'], **kwargs):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['article_api']['restore_articles'], ','.join(ids))
        _payload = {}
        return api, _payload

    @api_factory('delete')
    def delete_archived_article(self, id=1, **kwargs):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['delete_article'], str(id))
        _payload = {}
        return api, _payload

    @api_factory('post')
    def create_article(self, **kwargs):
        """
        Create an article.
        """
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['create_article'])
        _payload = {
            "selectedArticles": [],
            "selectedArticlesNos": [],
            "No": self.generate_random_number(),
            "name": self.generate_random_string(),
            "materialType": {
                "id": 1,
                "text": "Raw Material"
            },
            "selectedMaterialType": [
                {
                    "id": 1,
                    "text": "Raw Material"
                }
            ],
            "materialTypeId": 1,
            "dynamicFieldsValues": []
        }

        return api, _payload

    @api_factory('get')
    def list_testplans_by_article_and_materialtype(self, materialtype_id=1, article_id=1, **kwargs):
        api = '{}{}{}/{}'.format(self.url, self.END_POINTS['article_api']['list_testplans_by_article_and_materialtype'],
                                 article_id, materialtype_id)
        _payload = {}
        return api, _payload

    @api_factory('get')
    def list_articles_by_materialtype(self, materialtype_id=1, name='', is_archived=0, **kwargs):
        api = '{}{}{}/{}?name={}'.format(self.url, self.END_POINTS['article_api']['list_articles_by_materialtype'],
                                         materialtype_id, is_archived, name)
        _payload = {}
        return api, _payload

    @api_factory('get')
    def get_field_config(self):
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['get_field_config'])
        return api, {}

    @api_factory('put')
    def archive_field_config(self, filed_id):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['archive_field_config'], filed_id)
        return api, {}

    @api_factory('put')
    def restore_field_config(self, filed_id):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['restore_field_config'], filed_id)
        return api, {}


class ArticleAPI(ArticleAPIFactory):
    def get_all_articles_json(self, **kwargs):
        response, _ = self.get_all_articles(**kwargs)
        return response['articles']

    def get_first_record_with_data_in_attribute(self, attribute):
        articles_request, _ = self.get_all_articles()
        if (articles_request['status'] != 1) or (articles_request['count'] == 0):
            return False
        articles_records = articles_request['contacts']
        for article in articles_records:
            if article[attribute] != '':
                return article[attribute]

    def delete_active_article(self, id=1):
        response = self.archive_articles(ids=[str(id)])
        if response['status'] == 1 and response['message'] == 'delete_success':
            delete_response = self.delete_archived_article(id=id)
            if delete_response['status'] == 1 and delete_response['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_articles(ids=[str(id)])
                return False
        else:
            return False

    def get_active_articles_with_material_type(self):
        data = {}
        articles = self.get_all_articles()[0]['articles']
        for article in articles:
            material_type = article['materialType']
            if material_type not in data.keys():
                data[material_type] = []
            data[material_type].append(article['name'])
        return data

    def get_articles_with_no_testplans(self, **kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response[0]['articles']
        articles = [article for article in all_articles if len(article['testPlanNames']) < 1]
        return articles

    def get_articles_with_testplans(self, **kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response[0]['articles']

        articles = [article for article in all_articles if len(article['testPlanNames']) >= 1]
        return articles

    def archive_unit_config(self):
        return self.archive_field_config(filed_id=5)

    def restore_unit_config(self):
        return self.restore_field_config(filed_id=5)

    def archive_comment_config(self):
        return self.archive_field_config(filed_id=7)

    def restore_comment_config(self):
        return self.restore_field_config(filed_id=7)

    def archive_related_article_config(self):
        return self.archive_field_config(filed_id=18)

    def restore_related_article_config(self):
        return self.restore_field_config(filed_id=18)

    def archive_all_optional_fields(self):
        self.archive_unit_config()
        self.archive_comment_config()
        self.archive_related_article_config()

    def restore_all_optional_fields(self):
        self.restore_unit_config()
        self.restore_comment_config()
        self.restore_related_article_config()

    def quick_search_article(self, name):
        _filter = '{{"quickSearch":"{}","columns":["name"]}}'.format(name)
        return self.get_all_articles(filter=_filter)

    def get_article_with_material_type(self, material_type):
        material_type_id = GeneralUtilitiesAPI().get_material_id(material_type)
        articles, payload = self.get_all_articles(limit=500)
        self.info("search for article with material type {}".format(material_type))
        for article in articles['articles']:
            if article['materialType'] == material_type:
                return article['name']

        self.info("No article with requested material type, So create article")
        materialType = {"id": material_type_id, "text": material_type}
        api, payload = self.create_article(materialType=materialType,
                                           selectedMaterialType=[materialType],
                                           materialTypeId=int(material_type_id))
        if api['status'] == 1:
            return api['article']['name']

    def get_article_with_different_material(self, old_material):
        articles = self.get_all_articles_json()
        articles_list = []
        for article in articles:
            if article['materialType'] != old_material:
                articles_list.append(article)
        return articles_list

    def get_formatted_article_with_formatted_material_type(self, material_type, avoid_article=''):
        articles, payload = self.get_all_articles(limit=500)
        self.info("search for article with material type {}".format(material_type))
        for article in articles['articles']:
            if article['name'] == avoid_article:
                break
            elif article['materialType'] == material_type['text']:
                formatted_article = {'id': article['id'], 'name': article['name']}
                return formatted_article

        self.info("No article with requested material type, So create article")
        api, payload = self.create_article(materialType=material_type['text'],
                                           selectedMaterialType=[material_type],
                                           materialTypeId=int(material_type['id']))
        if api['status'] == 1:
            self.info('article has been created')
            return api['article']

    def get_random_article_articleID(self):
        selected_article = random.choice(self.get_all_articles(limit=30)[0]['articles'])
        return selected_article['name'], selected_article['id']

    def set_configuration(self):
        self.info('set article configuration')
        config_file = os.path.abspath('api_testing/config/articles.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)

