from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


class ArticleAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_articles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['list_all_articles'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
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


class ArticleAPI(ArticleAPIFactory):
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

    def get_articles_with_no_testplans(self,**kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response[0]['articles']
        articles = [article for article in all_articles if len(article['testPlanNames']) < 1]
        return articles

    def get_articles_with_testplans(self, **kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response.json()['articles']
        articles = [article for article in all_articles if len(article['testPlanNames']) >= 1]
        return articles

