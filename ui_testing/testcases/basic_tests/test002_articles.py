from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testplans_page import TestPlans
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.orders_api import OrdersAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from ui_testing.pages.login_page import Login
from api_testing.apis.users_api import UsersAPI
from parameterized import parameterized
from unittest import skip
import random, re


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
        self.default_filters_flags = {
            'name': False,
            'number': False,
            'created_at': False,
            'unit': False,
            'material_type': False,
            'changed_by': False,
            'test_plan': False,
        }

    def tearDown(self):
        if self.default_filters_flags['name'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_name')
            self.default_filters_flags['name'] = False

        if self.default_filters_flags['number'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_number')
            self.default_filters_flags['number'] = False

        if self.default_filters_flags['created_at'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_created_at')
            self.default_filters_flags['created_at'] = False

        if self.default_filters_flags['unit'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_unit')
            self.default_filters_flags['unit'] = False

        if self.default_filters_flags['material_type'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_material_type')
            self.default_filters_flags['material_type'] = False

        if self.default_filters_flags['changed_by'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_changed_by')
            self.default_filters_flags['changed_by'] = False

        if self.default_filters_flags['test_plan'] == True:
            self.article_page.toggle_default_filters(
                element1='article:default_filter_test_plan')
            self.default_filters_flags['test_plan'] = False

    @parameterized.expand(['save', 'cancel'])
    def test001_cancel_button_edit_unit(self, save):
        """
        New: Article: Save/Cancel button: After I edit unit field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.info('article_url : {}'.format(article_url))
        self.article_page.sleep_small()
        current_unit = self.article_page.get_unit()
        random_unit = self.generate_random_string()
        self.article_page.set_unit(random_unit)
        new_unit = self.article_page.get_unit()

        if 'save' == save:
            self.article_page.sleep_medium()
            self.article_page.save()
        else:
            self.article_page.sleep_medium()
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        article_unit = self.article_page.get_unit()
        if 'save' == save:
            self.info('Assert {} (new_unit) == {} (article_unit)'.format(new_unit, article_unit))
            self.assertEqual(new_unit, article_unit)
        else:
            self.info('Assert {} (current_unit) == {} (article_unit)'.format(current_unit, article_unit))
            self.assertEqual(current_unit, article_unit)

    @parameterized.expand(['save', 'cancel'])
    def test002_cancel_button_edit_no(self, save):
        """
        New: Article: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.info('article_url : {}'.format(article_url))
        self.article_page.sleep_small()
        current_no = self.article_page.get_no()
        random_no = self.generate_random_string()
        self.article_page.set_no(random_no)
        new_no = self.article_page.get_no()
        if 'save' == save:
            self.article_page.sleep_medium()
            self.article_page.save()
        else:
            self.article_page.sleep_medium()
            self.article_page.cancel(force=True)

        self.base_selenium.get(
            url=article_url, sleep=self.base_selenium.TIME_MEDIUM)
        self.base_selenium.scroll()
        article_no = self.article_page.get_no()

        if 'save' == save:
            self.info(' Assert {} (new_no) == {} (article_no)'.format(new_no, article_no))
            self.assertEqual(new_no, article_no)
        else:
            self.info(' Assert {} (current_no) == {} (article_no)'.format(current_no, article_no))
            self.assertEqual(current_no, article_no)

    @parameterized.expand(['save', 'cancel'])
    def test003_cancel_button_edit_name(self, save):
        """
        New: Article: Save/Cancel button: After I edit name then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.info('article_url : {}'.format(article_url))
        self.article_page.sleep_small()
        current_name = self.article_page.get_name()
        random_name = self.generate_random_string()
        self.article_page.set_name(random_name)
        new_name = self.article_page.get_name()
        if 'save' == save:
            self.article_page.sleep_medium()
            self.article_page.save()
        else:
            self.article_page.sleep_medium()
            self.article_page.cancel(force=True)

        self.base_selenium.get(
            url=article_url, sleep=self.base_selenium.TIME_MEDIUM)
        self.base_selenium.scroll()
        article_name = self.article_page.get_name()
        if 'save' == save:
            self.info('Assert {} (new_name) == {} (article_name)'.format(new_name, article_name))
            self.assertEqual(new_name, article_name)
        else:
            self.info('Assert {} (current_name) == {} (article_name)'.format(current_name, article_name))
            self.assertEqual(current_name, article_name)

    @parameterized.expand(['save', 'cancel'])
    def test004_cancel_button_edit_comment(self, save):
        """
        New: Article: Save/Cancel button: After I edit comment then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.info('article_url : {}'.format(article_url))
        self.article_page.sleep_small()
        current_comment = self.article_page.get_comment()
        new_comment = self.generate_random_string()
        self.article_page.set_comment(new_comment)
        if 'save' == save:
            self.article_page.sleep_medium()
            self.article_page.save()
        else:
            self.article_page.sleep_medium()
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        article_comment = self.article_page.get_comment()
        if 'save' == save:
            self.info('Assert {} (new_comment) == {} (article_comment)'.format(new_comment, article_comment))
            self.assertEqual(new_comment, article_comment)
        else:
            self.info('Assert {} (current_comment) == {} (article_comment)'.format(current_comment, article_comment))
            self.assertEqual(current_comment, article_comment)

    @skip('https://modeso.atlassian.net/browse/LIMSA-200')
    def test005_archived_articles_shoudnt_dispaly_in_test_plan(self):
        """
        New: Article: In case I archived any article this article shouldn't display in the test plan module when
        I create test plan or edit it

        LIMS-3668
        """
        article_created, payload = self.article_api.create_article()
        self.info(' Archive the article.')
        self.article_api.archive_articles(ids=[str(article_created['article']['id'])])
        self.test_plan_page.get_test_plans_page()
        self.info('Create test plan with the same material type.')
        self.test_plan_page.click_create_test_plan_button()
        self.article_page.sleep_small()
        self.test_plan_page.set_material_type(material_type=payload['materialType']['text'])
        self.article_page.sleep_tiny()
        self.info('Assert article is not existing in the list.')
        self.assertFalse(self.test_plan_page.is_article_existing(
            article=article_created['article']['name']))

    def test006_archived_articles_shoudnt_dispaly_in_order(self):
        """
        New: Article: Archived any article this article shouldn't display in the order module

        LIMS-3668
        """
        api, payload = self.article_api.create_article()
        self.article_api.archive_articles(ids=[str(api['article']['id'])])
        orders, payload = self.order_api.get_all_orders(limit=20)
        random_order = random.choice(orders['orders'])
        self.info('{}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        self.order_page.set_material_type_of_first_suborder(material_type='Raw Material', sub_order_index=0)
        self.order_page.confirm_popup()
        self.order_page.set_article(article=api['article']['name'])
        self.assertFalse(
            self.order_page.is_article_existing(article=api['article']['name']))

    @skip('https://modeso.atlassian.net/browse/LIMSA-200')
    def test007_created_article_appear_in_test_plan(self):
        """
        New: Article/Test plan: Any article I created should appear in the test plan according to the materiel type.

        LIMS-3581
        """
        article_created, payload = self.article_api.create_article()
        self.test_plan_page.get_test_plans_page()
        self.test_plan_page.click_create_test_plan_button()
        self.test_plan_page.set_material_type(material_type=payload['materialType']['text'])
        self.article_page.sleep_tiny()
        self.assertTrue(
            self.test_plan_page.is_article_existing(article=article_created['article']['name']))

    @skip('https://modeso.atlassian.net/browse/LIMSA-200')
    def test008_create_article_with_test_plan_search_by_test_plan(self):
        """
        In case I create test plan with the article that I created, this
        test plan should display in the table view

        LIMS-3583
        """
        article_created = self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan_page.get_test_plans_page()
        self.test_plan_page.create_new_test_plan(material_type=article_created['material_type'],
                                                 article=article_created['name'])
        self.article_page.get_articles_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=self.test_plan_page.test_plan_name)[0]
        self.assertIn(self.test_plan_page.test_plan_name, article.text)

        self.test_plan_page.get_test_plans_page()
        self.test_plan_page.get_test_plan_edit_page(name=self.test_plan_page.test_plan_name)

        self.test_plan_page.clear_article()
        self.test_plan_page.set_article(article='All')
        self.test_plan.save(save_btn='test_plan:save_btn')
        self.article_page.get_articles_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=article_created['article']['name'])[0]
        self.article_page.sleep_small()
        self.assertNotIn(self.test_plan_page.test_plan_name, article.text)

    @skip('https://modeso.atlassian.net/browse/LIMSA-200')
    def test009_create_article_with_test_plan_filter_by_test_plan(self):
        """
        In case I create test plan with the article that I created, user could filter with test plan

        LIMS-3583
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan_page.get_test_plans_page()
        self.test_plan_page.create_new_test_plan(material_type=self.article_page.article_material_type,
                                                 article=self.article_page.article_name)
        self.article_page.get_articles_page()
        self.article_page.sleep_small()

        self.article_page.open_filter_menu()
        self.article_page.filter_article_by(filter_element='article:filter_test_plan',
                                            filter_text=self.test_plan_page.test_plan_name, field_type="drop_down")
        article = self.article_page.result_table()[0]
        self.info('Assert user could filter with test plan.')
        self.assertIn(self.test_plan_page.test_plan_name, article.text)

    def test010_archive_articles(self):
        """
        New: Article: Archive Approach: I can archive/restore any article successfully

        LIMS-3587
        """
        selected_articles_data, _ = self.article_page.select_random_multiple_table_rows()
        self.article_page.archive_selected_articles()
        self.article_page.get_archived_articles()
        for article in selected_articles_data:
            article_name = article['Article Name']
            self.info('{} article should be activated.'.format(article_name))
            self.assertTrue(self.article_page.is_article_in_table(value=article_name))

    def test011_restore_articles(self):
        """
        New: Article: Restore Approach: I can archive/restore any article successfully

        LIMS-3587
        """
        article_names = []
        self.article_page.get_archived_articles()
        selected_articles_data, _ = self.article_page.select_random_multiple_table_rows()
        for article in selected_articles_data:
            article_names.append(article['Article Name'])

        self.article_page.restore_selected_articles()
        self.article_page.get_active_articles()
        for article_name in article_names:
            self.assertTrue(self.article_page.is_article_in_table(value=article_name))

    def test012_create_new_material_type(self):
        """
        Article: Materiel type Approach: make sure you can create new materiel type
        & this materiel type displayed correct according to this article.

        LIMS-3582
        """
        material_type = self.generate_random_string()
        self.article_page.create_new_article(material_type=material_type)
        self.test_plan_page.get_test_plans_page()
        self.test_plan_page.click_create_test_plan_button()
        self.test_plan_page.set_material_type(material_type=material_type)
        self.article_page.sleep_tiny()
        self.assertTrue(self.test_plan_page.is_article_existing(article=self.article_page.article_name))

    def test013_article_search(self):
        """
        New: Articles: Search Approach: I can search by any field in the table view

        LIMS-3594
        """
        row = self.article_page.get_random_article_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or \
                    row_data[column] == '-' or not (row_data[column]):
                continue
            multiple_testplans = False
            if "," in row_data[column]:  # for multiple testplans only search for one of them
                row_data[column] = row_data[column].split(',', 1)[0]
                multiple_testplans = True

            self.info('search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                    search_result)
                if multiple_testplans:
                    search_data[column] = search_data[column].split(',', 1)[0]
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test014_green_border(self):
        """
        New: All modules: Creation Approach: Green border displayed when I create new record

        LIMS-3597
        """
        self.article_page.create_new_article(sleep=False, material_type='Raw Material')
        self.article_page.sleep_small()
        self.assertEqual(self.base_selenium.get_text(element='general:alert_confirmation'),
                         'Successfully created')

    def test015_create_full_options_article(self):
        """
        New: Articles: Creation Approach: I can create new article successfully

        LIMS-3575
        """
        self.article_page.create_new_article(full_options=True, material_type='Raw Material')
        self.article_page.sleep_tiny()
        article_text = self.article_page.search(value=self.article_page.article_name)[0].text

        self.assertIn(self.article_page.article_unit, article_text)
        self.assertIn(self.article_page.article_comment, article_text)
        self.assertIn(self.article_page.article_material_type, article_text)

    def test016_delete_article_with_test_plan(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        """
        test_plan = self.test_plan_api.create_testplan_with_article_not_all()
        self.info("test plan created with article No {}".format(test_plan['selectedArticleNos'][0]['name']))
        self.article_page.filter_and_select(test_plan['selectedArticleNos'][0]['name'])
        self.info("Archive article")
        self.article_page.archive_selected_articles()
        self.info("Navigate to archived  articles page")
        self.article_page.get_archived_articles()
        self.article_page.filter_and_select(test_plan['selectedArticleNos'][0]['name'])
        self.info("delete selected article")
        self.assertFalse(self.article_page.delete_selected_article())
        row = self.article_page.get_the_latest_row_data()
        self.assertEqual(row['Article No.'].replace("'", ""), test_plan['selectedArticleNos'][0]['name'])

    #@skip('waiting create order update')
    def test017_delete_article_with_order(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        """
        response, payload = self.order_api.create_new_order()
        self.assertEqual(response['status'], 1, "order not created")
        article_number = self.article_api.get_article_form_data(
            id=payload[0]['article']['id'])[0]['article']['No']
        self.info("order created with article No {}".format(article_number))
        self.article_api.archive_articles(ids=[str(payload[0]['article']['id'])])
        self.article_page.get_archived_articles()
        self.article_page.filter_and_select(article_number)
        self.info('delete this article, should fail.')
        self.assertFalse(self.article_page.delete_selected_article())
        row = self.article_page.get_the_latest_row_data()
        self.assertEqual(row['Article No.'].replace("'", ""), article_number)

    @skip('https://modeso.atlassian.net/browse/LIMSA-201')
    def test018_download_article_sheet(self):
        """
        New: Articles: XSLX File: I can download all the data in the table view in the excel sheet

        LIMS:3589-case of all sheet
        """
        self.info(' * Download XSLX sheet')
        self.article_page.download_xslx_sheet()
        rows_data = list(filter(None, self.article_page.get_table_rows_data()))
        for index in range(len(rows_data)):
            self.info(' * Comparing the article no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.article_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    @parameterized.expand(['ok', 'cancel'])
    def test019_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.info('create new article.')
        self.article_page.sleep_tiny()
        self.base_selenium.click(element='articles:new_article')
        self.article_page.sleep_small()
        # click on Overview, this will display an alert to the user
        self.article_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.article_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(),
                             '{}articles'.format(self.base_selenium.url))
            self.info('clicking on Overview confirmed')
        else:
            self.article_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(),
                             '{}articles/add'.format(self.base_selenium.url))
            self.info('clicking on Overview cancelled')

    def test020_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.info('article_url : {}'.format(article_url))
        # click on Overview, it will redirect you to articles' page
        self.info('click on Overview')
        self.article_page.click_overview()
        self.article_page.sleep_small()
        self.assertEqual(self.base_selenium.get_url(),
                         '{}articles'.format(self.base_selenium.url))
        self.info('clicking on Overview confirmed')

    @skip('we will skip it until we fix the issue')
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

    @skip('we will skip it until we fix the issue')
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

    @skip('we will skip it until we teh issue')
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
    @skip('we will skip it until we fix the issue')
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
            self.info(' open article edit page')
            self.article_page.open_edit_page(row=self.article_page.get_random_article_row())
        else:
            self.info(' open article create page')
            self.base_selenium.click(element='articles:new_article')
            self.article_page.wait_until_page_is_loaded()
        self.info(' assert unit field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:unit'))

        self.info(' assert comment field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:comment'))

        self.info(' assert related article field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_not_exist('article:related_article'))

    @parameterized.expand(['edit', 'create'])
    @skip('we will skip it until we decide that we fix the issue')
    def test025_restore_optional_config_fields_effect_(self, page):
        """
            LIMS-4123
            part-3:
                User should be able to archive/restore field
            steps:
             - restore options using api
             - assert all fields have been displayed from the create/edit page
        """
        self.info('archive all option fields via api')
        self.article_api.restore_all_optional_fields()

        if page == "edit":
            self.info(' open article edit page')
            self.article_page.open_edit_page(row=self.article_page.get_random_article_row())
        else:
            self.info(' open article create page')
            self.base_selenium.click(element='articles:new_article')
            self.article_page.wait_until_page_is_loaded()
        self.info(' assert unit field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_exist('article:unit'))

        self.info(' assert comment field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_exist('article:comment'))

        self.info(' assert related article field is not existing in article page')
        self.assertTrue(self.base_selenium.check_element_is_exist('article:related_article'))

    @parameterized.expand([('name', 'Article Name'),
                           ('number', 'Article No.'),
                           ('unit', 'Unit'),
                           ('created_at', 'Created On'),
                           ('material_type', 'Material Type')])
    def test026_filter_article_by_any_field(self, filter_name, header):
        """
        New: Article: Filter Approach: I can filter by any static field & and also from the default filter.

        LIMS-3595
        """
        # set default material type and field type
        material_type = 'Raw Material'
        field_type = 'text'
        full_options = False
        # set the material type to None in case of material type filter to test with random material type name
        if filter_name == 'material_type':
            material_type = None
            field_type = 'drop_down'
        # use full options in case of unit field
        if filter_name == 'unit':
            full_options = True
        # create new article with full options
        article = self.article_page.create_new_article(
            material_type=material_type, full_options=full_options)
        # open article table page and open the filter menu
        self.assertTrue(article, 'article not created')
        self.article_page.sleep_medium()
        self.article_page.open_filter_menu()
        # filter the article and get the result
        article_results = self.article_page.filter_article_by(filter_element='article:filter_{}'.format(
            filter_name), filter_text=article[filter_name], field_type=field_type)
        for article_result in article_results:
            self.assertEqual(article[filter_name].replace("'", ""), article_result[header].replace("'", ""))

    def test027_filter_article_by_changed_by_filter(self):
        """
        New: Article: Filter Approach: I can filter by changed by.

        LIMS-3595
        """
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.article_page.sleep_tiny()
        self.login_page.logout()
        self.article_page.sleep_tiny()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.article_page.get_articles_page()
        self.article_page.sleep_tiny()
        article = self.article_page.create_new_article()['name']
        self.info('New article is created successfully with name: {}'.format(article))
        self.article_page.set_all_configure_table_columns_to_specific_value(
            always_hidden_columns=['selectedArticles'])
        # filter the article and get the results
        self.article_page.apply_filter_scenario(filter_element='article:filter_changed_by',
                                                filter_text=payload['username'])
        self.article_page.sleep_tiny()
        result_articles = self.base_selenium.get_rows_cells_dict_related_to_header()
        for article_result in result_articles:
            self.assertEqual(article, article_result['Article Name'])
            self.assertEqual(payload['username'], article_result['Changed By'])

    def test028_article_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        articles_response = self.article_api.get_all_articles()
        articles = articles_response[0]['articles']
        article_name = random.choice(articles)['name']
        search_results = self.article_page.search(article_name)
        self.article_page.sleep_medium()
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Article Name'] == article_name:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(article_name, search_data['Article Name'])
        # Navigate to test plan page
        self.info('navigate to test plans page')
        self.test_plan_page.get_test_plans_page()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))

    def test029_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        self.article_page.sleep_medium()
        assert (self.article_page.deselect_all_configurations(), False)
