from UI_TESTING.testcases.base_test import BaseTest
from UI_TESTING.pages.login_page import Login


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()

    def test001_create_new_article(self):
        self.login_page.login(username=self.username, password=self.password)
