from ui_testing.apis.base_api import BaseAPI


class ArticlesAPI(BaseAPI):
    def get_article(self, article_id):
        api = "{}/api/articles/get/{}".format(self.url, article_id)
        return self.session.get(api)

