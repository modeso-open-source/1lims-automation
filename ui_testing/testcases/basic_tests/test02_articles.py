from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.articles import Articles
from parameterized import parameterized


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Articles()

        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
    #
    # def test001_create_new_article(self):
    #     self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
    #
    # @parameterized.expand([('edit_unit', 'editText'),
    #                        ('edit_no', 20),
    #                        ('edit_name', 'editName'),
    #                        ('edit_comment', 'editComment')])
    def test002_cancel_button_edit_unit(self):
        """
        New: Article: Cancel button: After I edit unit field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        :return: 
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_unit = self.article_page.get_unit()
        self.article_page.edit_unit(self.generate_random_string())
        self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url)
        self.assertEqual(current_unit, self.article_page.get_unit())

    def test003_cancel_button_edit_no(self):
        """
        New: Article: Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()

        current_no = self.article_page.get_no()
        self.article_page.edit_no(self.generate_random_string())
        self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url)
        self.assertEqual(current_no, self.article_page.get_no())

    def test004_cancel_button_edit_name(self):
        """
        New: Article: Cancel button: After I edit name then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()

        current_name = self.article_page.get_name()
        self.article_page.edit_name(self.generate_random_string())
        self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url)
        self.assertEqual(current_name, self.article_page.get_unit())

    def test005_cancel_button_edit_comment(self):
        """
        New: Article: Cancel button: After I edit comment then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_comment = self.article_page.get_comment()
        self.article_page.edit_comment(self.generate_random_string())
        self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url)
        self.assertEqual(current_comment, self.article_page.get_unit())

