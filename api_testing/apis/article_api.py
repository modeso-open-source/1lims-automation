from api_testing.apis.base_api import BaseAPI


class ArticleAPI(BaseAPI):
    def get_all_articles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['list_all_articles'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers)
        self.info('Status code: {}'.format(response.status_code))
        return response

