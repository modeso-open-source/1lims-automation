from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testplans_page import TestPlans
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.orders_api import OrdersAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from parameterized import parameterized
from unittest import skip
from nose.plugins.attrib import attr


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.article_page = Article()
        self.article_api = ArticleAPI()
        self.test_plan_api = TestPlanAPI()
        self.test_plans_page = TestPlans()
        self.test_plan_page = TstPlan()
        self.orders_page = Orders()
        self.order_api = OrdersAPI()
        self.order_page = Order()
        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)
        self.article_api.set_configuration()
        self.article_page.get_articles_page()

    @attr(series=True)
    def test021_user_archive_optional_config_fields(self):
        """
            LIMS-4123
            part-1:
                User should be able to archive/restore field
            steps:
             - restore all fields using API
             - archive it via the UI
             - assert all fields have been archived
        """
        self.info('restore all option fields via api')
        self.article_api.restore_all_optional_fields()

        self.info('archive all option fields via ui')
        self.article_page.archive_all_optional_fields()

        self.info('assert all option fields have been archived')
        self.assertFalse(self.article_page.is_field_active('unit'))
        self.assertFalse(self.article_page.is_field_active('comment'))
        self.assertFalse(self.article_page.is_field_active('related article'))

    @attr(series=True)
    def test022_user_restore_optional_config_fields(self):
        """
            LIMS-4123
            part-2:
                User should be able to archive/restore field
            steps:
             - archive all fields using API
             - restore it via the UI
             - assert all fields have been restored
        """
        self.info('archive all option fields via api')
        self.article_api.archive_all_optional_fields()

        self.info('restore all option fields via ui')
        self.article_page.restore_optional_fields()

        self.info('assert all option fields have been archived')
        self.assertFalse(self.article_page.is_field_restore('unit'))
        self.assertFalse(self.article_page.is_field_restore('comment'))
        self.assertFalse(self.article_page.is_field_restore('related article'))

    @attr(series=True)
    def test023_archive_optional_config_fields_does_not_effect_table(self):
        """
            LIMS-4123
            part-4:
                User should be able to archive/restore field
            steps:
             - archive options using api
             - assert all fields have been displayed in table
        """
        self.info('archive all option fields via api')
        self.article_api.archive_all_optional_fields()

        self.info(' open article table')
        self.article_page.get_articles_page()
        article_headers = self.base_selenium.get_table_head_elements('general:table')
        article_headers_text = [header.text for header in article_headers]

        self.info(' assert comment field existance in the table')
        self.assertIn('Comment', article_headers_text)

        self.info(' assert unit field existance in the table')
        self.assertIn('Unit', article_headers_text)

    @parameterized.expand(['edit', 'create'])
    @attr(series=True)
    def test024_archive_optional_config_fields_effect_(self, page):
        """
            LIMS-4123
            part-3:
                User should be able to archive/restore field
            steps:
             - archive options using api
             - assert all fields have been not displayed from the create/edit page
        """
        self.info('archive all option fields via api')
        self.article_api.archive_all_optional_fields()

        if page == "edit":
            self.info('open article edit page')
            self.article_page.open_edit_page(row=self.article_page.get_random_article_row())
        else:
            self.info('open article create page')
            self.base_selenium.click(element='articles:new_article')
            self.article_page.wait_until_page_is_loaded()
        self.info(' assert unit field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:unit'))

        self.info(' assert comment field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:comment'))

        self.info(' assert related article field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:related_article'))

    @parameterized.expand(['edit', 'create'])
    @attr(series=True)
    def test025_restore_optional_config_fields_effect_(self, page):
        """
            LIMS-4123
            part-3:
                User should be able to archive/restore field
            steps:
             - restore options using api
             - assert all fields have been displayed from the create/edit page
        """
        self.info('restore all option fields via api')
        self.article_api.restore_all_optional_fields()

        if page == "edit":
            self.info('open article edit page')
            self.article_page.open_edit_page(row=self.article_page.get_random_article_row())
        else:
            self.info('open article create page')
            self.base_selenium.click(element='articles:new_article')
            self.article_page.wait_until_page_is_loaded()
        self.info('assert unit field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_exist('article:unit'))

        self.info('assert comment field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_exist('article:comment'))

        # self.info('assert related article field is not existing in article page')
        # self.assertTrue(self.base_selenium.check_element_is_exist('article:related_article'))
