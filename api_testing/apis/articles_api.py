from api_testing.apis.base_api import BaseAPI


class ArticlesAPI(BaseAPI):
    def get_article(self, article_id):
        api = "{}{}{}".format(self.url, self.END_POINTS['article']['get_article'], article_id)
        return self.session.get(api)

