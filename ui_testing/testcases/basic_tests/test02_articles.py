from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.articles import Articles
from parameterized import parameterized
import time


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Articles()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')

    @parameterized.expand(['save', 'cancel'])
    def test002_cancel_button_edit_unit(self, save):
        """
        New: Article: Save/Cancel button: After I edit unit field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_unit = self.article_page.get_unit()
        new_unit = self.generate_random_string()
        self.article_page.edit_unit(new_unit)
        if 'save' == save:
            self.article_page.save_edit()
        else:
            self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_unit, self.article_page.get_unit())
        else:
            self.assertEqual(current_unit, self.article_page.get_unit())

    @parameterized.expand(['save', 'cancel'])
    def test003_cancel_button_edit_no(self, save):
        """
        New: Article: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_no = self.article_page.get_no()
        new_no = self.generate_random_string()
        self.article_page.edit_no(new_no)
        if 'save' == save:
            self.article_page.save_edit()
        else:
            self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_no, self.article_page.get_no())
        else:
            self.assertEqual(current_no, self.article_page.get_no())

    @parameterized.expand(['save', 'cancel'])
    def test004_cancel_button_edit_name(self, save):
        """
        New: Article: Save/Cancel button: After I edit name then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()

        current_name = self.article_page.get_name()
        new_name = self.generate_random_string()
        self.article_page.edit_name(new_name)

        if 'save' == save:
            self.article_page.save_edit()
        else:
            self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_name, self.article_page.get_name())
        else:
            self.assertEqual(current_name, self.article_page.get_name())

    @parameterized.expand(['save', 'cancel'])
    def test005_cancel_button_edit_comment(self, save):
        """
        New: Article: Save/Cancel button: After I edit comment then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_comment = self.article_page.get_comment()
        new_comment = self.generate_random_string()
        self.article_page.edit_comment(new_comment)
        if 'save' == save:
            self.article_page.save_edit()
        else:
            self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_comment, self.article_page.get_comment())
        else:
            self.assertEqual(current_comment, self.article_page.get_comment())

    @parameterized.expand(['cancel', 'save'])
    def test006_cancel_button_edit_material_type(self, save):
        """
        New: Article: Save/Cancel button: After I edit material_type then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_article_page()
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        time.sleep(2)
        current_material_type = self.article_page.get_material_type()
        self.article_page.edit_material_type(random=True)
        new_material_type = self.article_page.get_material_type()
        if 'save' == save:
            self.article_page.save_edit()
        else:
            self.article_page.cancel_edit(force=True)

        self.base_selenium.get(url=article_url, sleep=5)

        if 'save' == save:
            self.assertEqual(new_material_type, self.article_page.get_material_type())
        else:
            self.assertEqual(current_material_type, self.article_page.get_material_type())

