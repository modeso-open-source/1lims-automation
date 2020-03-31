from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.order_page import Order
from api_testing.apis.article_api import ArticleAPI
from parameterized import parameterized
from unittest import skip
import random, re


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.article_page = Article()
        self.article_api = ArticleAPI()
        self.test_plan = TstPlan()
        self.order_page = Order()
        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)

        self.article_page.get_articles_page()
        self.archived_optional_fields_flag = False
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
        if self.archived_optional_fields_flag:  # to restore the UI
            self.article_page.get_articles_page()
            self.article_page.archive_restore_optional_fields(restore=True)
            self.archived_optional_fields_flag = False

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

        super().tearDown()

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
        self.article_page.info('article_url : {}'.format(article_url))
        current_unit = self.article_page.get_unit()
        new_unit = self.generate_random_string()
        self.article_page.set_unit(new_unit)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)
        article_unit = self.article_page.get_unit()
        if 'save' == save:
            self.article_page.info(
                'Assert {} (new_unit) == {} (article_unit)'.format(new_unit, article_unit))
            self.assertEqual(new_unit, article_unit)
        else:
            self.article_page.info(
                'Assert {} (current_unit) == {} (article_unit)'.format(current_unit, article_unit))
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
        self.article_page.info('article_url : {}'.format(article_url))
        current_no = self.article_page.get_no()
        new_no = self.generate_random_string()
        self.article_page.set_no(new_no)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(
            url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        article_no = self.article_page.get_no()
        if 'save' == save:
            self.article_page.info(
                ' Assert {} (new_no) == {} (article_no)'.format(new_no, article_no))
            self.assertEqual(new_no, article_no)
        else:
            self.article_page.info(
                ' Assert {} (current_no) == {} (article_no)'.format(current_no, article_no))
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
        self.article_page.info('article_url : {}'.format(article_url))
        current_name = self.article_page.get_name()
        new_name = self.generate_random_string()
        self.article_page.set_name(new_name)

        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(
            url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        article_name = self.article_page.get_name()
        if 'save' == save:
            self.article_page.info(
                'Assert {} (new_name) == {} (article_name)'.format(new_name, article_name))
            self.assertEqual(new_name, article_name)
        else:
            self.article_page.info(
                'Assert {} (current_name) == {} (article_name)'.format(current_name, article_name))
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
        self.article_page.info(
            'article_url : {}'.format(article_url))
        current_comment = self.article_page.get_comment()
        new_comment = self.generate_random_string()
        self.article_page.set_comment(new_comment)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(
            url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        article_comment = self.article_page.get_comment()
        if 'save' == save:
            self.article_page.info(
                'Assert {} (new_comment) == {} (article_comment)'.format(new_comment, article_comment))
            self.assertEqual(new_comment, article_comment)
        else:
            self.article_page.info(
                'Assert {} (current_comment) == {} (article_comment)'.format(current_comment, article_comment))
            self.assertEqual(current_comment, article_comment)

    @parameterized.expand(['save', 'cancel'])
    def test005_cancel_button_edit_material_type(self, save):
        """
        New: Article: Save/Cancel button: After I edit material_type
        then press on cancel button,a pop up will appear that the
        data will not saved

        LIMS-3586
        LIMS-3576
        """
        article_id = random.choice(self.article_api.get_articles_with_no_testplans())["id"]
        # open edit page
        a = "{}articles/edit/" + str(article_id)
        edit_page_url = a.format(self.base_selenium.url)
        self.base_selenium.get(url=edit_page_url)
        current_material_type = self.article_page.get_material_type()
        new_material_type = self.article_page.set_material_type(random=True)

        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=edit_page_url, sleep=5)
        article_material = self.article_page.get_material_type()
        if 'save' == save:
            self.info('Assert {} (new_material_type) == {} (article_material_type)'.format(
                new_material_type, article_material))
            self.assertEqual(new_material_type, article_material)
            self.assertNotEqual(current_material_type, article_material)  # make sure that material type edited right
        else:
            self.info('Assert {} (current_material_type) == {} (article_material_type)'.format(
                current_material_type, article_material))
            self.assertEqual(current_material_type, article_material)

    def test006_archived_articles_shoudnt_dispaly_in_test_plan(self):
        """
        New: Article: In case I archived any article this article shouldn't display in the test plan module when
         I create test plan or edit it

        LIMS-3668
        """
        create_response, _ = self.article_api.create_article()
        self.base_selenium.LOGGER.info(' Archive the article.')
        archive_response, _ = self.article_api.archive_articles(ids=[str(create_response['article']['id'])])
        self.test_plan.get_test_plans_page()
        self.base_selenium.LOGGER.info(
            'Create test plan with the same material type.')
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type="Raw Material")
        self.article_page.sleep_tiny()
        self.base_selenium.LOGGER.info(
            'Assert article is not existing in the list.')
        self.assertFalse(self.test_plan.is_article_existing(article=create_response['article']['name']))

    @skip('refactor order page')
    def test007_archived_articles_shoudnt_dispaly_in_order(self):
        """
        New: Article: Archived any article this article shouldn't display in the order module

        LIMS-3668
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.article_page.archive_article(name=self.article_page.article_name)
        self.order_page.get_orders_page()
        self.order_page.click_create_order_button()
        self.order_page.set_new_order()
        self.order_page.set_material_type(
            material_type=self.article_page.article_material_type)
        self.article_page.sleep_tiny()
        self.assertFalse(self.order_page.is_article_existing(
            article=self.article_page.article_name))

    def test008_created_article_appear_in_test_plan(self):
        """
        New: Article/Test plan: Any article I created should appear in the test plan according to the materiel type.

        LIMS-3581
        """
        create_response, _ = self.article_api.create_article()
        self.test_plan.get_test_plans_page()
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type="Raw Material")
        self.article_page.sleep_tiny()
        self.assertTrue(self.test_plan.is_article_existing(article=create_response['article']['name']))

    def test009_create_article_with_test_plan_search_by_test_plan(self):
        """
        In case I create test plan with the article that I created, this test plan should display in the table view

        LIMS-3583
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name)
        self.article_page.get_articles_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=self.test_plan.test_plan_name)[0]
        self.assertIn(self.test_plan.test_plan_name, article.text)

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name=self.test_plan.test_plan_name)

        self.test_plan.clear_article()
        self.test_plan.set_article(article='All')
        self.test_plan.save()
        self.article_page.get_articles_page()
        article = self.article_page.search(self.article_page.article_name)[0]
        self.assertNotIn(self.test_plan.test_plan_name, article.text)

    def test010_create_article_with_test_plan_filter_by_test_plan(self):
        """
        In case I create test plan with the article that I created, user could filter with test plan

        LIMS-3583
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name)
        self.article_page.get_articles_page()
        self.article_page.sleep_small()

        self.article_page.open_filter_menu()
        self.article_page.filter_article_by(filter_element='article:filter_test_plan',
                                            filter_text=self.test_plan.test_plan_name, field_type="drop_down")
        article = self.article_page.result_table()[0]
        self.article_page.info('Assert user could filter with test plan.')
        self.assertIn(self.test_plan.test_plan_name, article.text)

    def test011_archive_articles(self):
        """
        New: Article: Archive Approach: I can archive/restore any article successfully

        LIMS-3587
        """
        selected_articles_data, _ = self.article_page.select_random_multiple_table_rows()
        self.article_page.archive_selected_articles()
        self.article_page.get_archived_articles()
        for article in selected_articles_data:
            article_name = article['Article Name']
            self.article_page.info('{} article should be activated.'.format(article_name))
            self.assertTrue(self.article_page.is_article_in_table(value=article_name))

    def test012_restore_articles(self):
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

    def test013_create_new_material_type(self):
        """
        Article: Materiel type Approach: make sure you can create new materiel type
        & this materiel type displayed correct according to this article.

        LIMS-3582
        """
        material_type = self.generate_random_string()
        self.article_page.create_new_article(material_type=material_type)
        self.test_plan.get_test_plans_page()
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type=material_type)
        self.article_page.sleep_tiny()
        self.assertTrue(self.test_plan.is_article_existing(article=self.article_page.article_name))

    def test014_article_search(self):
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

    def test015_green_border(self):
        """
        New: All modules: Creation Approach: Green border displayed when I create new record

        LIMS-3597
        """
        self.article_page.create_new_article(sleep=False, material_type='Raw Material')
        self.assertEqual(self.base_selenium.get_text(element='articles:alert_confirmation'),
                         'Successfully created')

    def test016_create_full_options_article(self):
        """
        New: Articles: Creation Approach: I can create new article successfully

        LIMS-3575
        """
        self.article_page.create_new_article(full_options=True, material_type='Raw Material')
        article_text = self.article_page.search(value=self.article_page.article_name)[0].text
        self.assertIn(self.article_page.article_unit, article_text)
        self.assertIn(self.article_page.article_comment, article_text)
        self.assertIn(self.article_page.article_material_type, article_text)

    def test017_delete_article_with_test_plan(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        """
        # get article with testPlan
        article_name = random.choice(self.article_api.get_articles_with_testplans(limit=100))["name"]
        article = self.article_page.search(value=article_name)[0]
        # archive article
        self.article_page.click_check_box(source=article)
        self.article_page.archive_selected_articles()
        # get archived articles, select our article then delete it
        self.article_page.get_archived_articles()
        archived_article = self.article_page.search(value=article_name)[0]
        self.article_page.click_check_box(source=archived_article)
        self.assertFalse(self.article_page.delete_selected_article())

    @skip('Refactoring order page')
    def test018_delete_article_with_order(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        """
        self.article_page.info('Create new article with Raw Material.')
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.article_page.info('Create new test plan with {} article.'.format(self.article_page.article_name))
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name,
                                            test_unit='Qualitative')
        self.order_page.get_orders_page()
        self.order_page.click_create_order_button()
        self.article_page.info('Create new order with {} article.'.format(self.article_page.article_name))
        self.order_page.create_new_order(article=self.article_page.article_name,
                                         material_type=self.article_page.article_material_type,
                                         test_plans=[self.test_plan.test_plan_name])

        self.article_page.get_articles_page()
        self.article_page.sleep_small()
        self.article_page.info('Search for active article with {} test plan.'.format(self.test_plan.test_plan_name))
        search_results = self.article_page.search(value=self.test_plan.test_plan_name)
        self.assertGreater(len(search_results), 1,
                           " * There is no search results for it, Report a bug.")

        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                search_result)
            if self.test_plan.test_plan_name in search_data['Test Plans']:
                break
            self.base_selenium.LOGGER.debug(
                ' Article test plan : {} '.format(search_data['Test Plans']))
        else:
            raise ValueError(" There is no active article with {} test plan".format(
                self.test_plan.test_plan_name))
        self.article_page.info('Archive this article.')
        self.article_page.click_check_box(source=search_result)
        self.article_page.archive_selected_articles()

        self.article_page.get_archived_articles()
        self.base_selenium.LOGGER.info(
            ' + Search for archived article with {} test plan.'.format(self.test_plan.test_plan_name))
        search_results = self.article_page.search(
            value=self.test_plan.test_plan_name)
        self.assertGreater(len(search_results), 1,
                           " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                search_result)
            if self.test_plan.test_plan_name in search_data['Test Plans']:
                break
            self.base_selenium.LOGGER.debug(
                ' Article test plan : {} '.format(search_data['Test Plans']))
        else:
            raise ValueError(" There is no archived article with {} test plan".format(
                self.test_plan.test_plan_name))

        self.base_selenium.LOGGER.info(' + Delete this article, should fail.')
        self.article_page.click_check_box(source=search_result)
        self.assertFalse(self.article_page.delete_selected_article())

    def test019_download_article_sheet(self):
        """
        New: Articles: XSLX File: I can download all the data in the table view in the excel sheet

        LIMS:3589-case of all sheet
        """
        self.info(' * Download XSLX sheet')
        self.article_page.download_xslx_sheet()
        rows_data = self.article_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.info(' * Comparing the article no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.article_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    @parameterized.expand(['ok', 'cancel'])
    def test020_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.article_page.info('create new article.')
        self.base_selenium.click(element='articles:new_article')
        self.article_page.sleep_tiny()
        # click on Overview, this will display an alert to the user
        self.article_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.article_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(),
                             '{}articles'.format(self.base_selenium.url))
            self.article_page.info('clicking on Overview confirmed')
        else:
            self.article_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(),
                             '{}articles/add'.format(self.base_selenium.url))
            self.article_page.info('clicking on Overview cancelled')

    def test021_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.article_page.info('article_url : {}'.format(article_url))
        # click on Overview, it will redirect you to articles' page
        self.article_page.info('click on Overview')
        self.article_page.click_overview()
        self.article_page.sleep_small()
        self.assertEqual(self.base_selenium.get_url(),
                         '{}articles'.format(self.base_selenium.url))
        self.article_page.info('clicking on Overview confirmed')

    def test022_user_hide_any_optional_field_is_not_affecting_the_table(self):
        """
        New: Articles: Optional fields: User can hide/show any optional field in Edit/Create form

        LIMS:4123
        :return:
        """
        # archive the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.archived_optional_fields_flag = True  # to restore the UI in the tearDown

        # check if the fields still exist in the table
        self.article_page.info('+ Open article table')
        self.article_page.get_articles_page()
        article_headers = self.base_selenium.get_table_head_elements(
            'general:table')
        article_headers_text = [header.text for header in article_headers]

        self.article_page.info('+ Check Comment field existance in the table')
        self.assertIn('Comment', article_headers_text)

        self.article_page.info('+ Check Unit field existance in the table')
        self.assertIn('Unit', article_headers_text)
        # ignore related article since it shouldn't display in the table anyway

    def test023_user_hide_any_optional_field_in_create_form(self):
        """
        New: Articles: Optional fields: User can hide/show any optional field in Edit/Create form

        LIMS:4123
        :return:
        """
        # archive the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.archived_optional_fields_flag = True  # to restore the UI in the tearDown

        # open create page
        self.article_page.get_articles_page()
        self.article_page.info('+ Open article create')
        self.base_selenium.click(element='articles:new_article')
        self.article_page.sleep_small()

        self.article_page.info('+ Check Unit field existance in create page')
        self.assertFalse(
            self.base_selenium.check_element_is_exist('article:unit'))

        self.article_page.info(
            '+ Check Comment field existance in create page')
        self.assertFalse(
            self.base_selenium.check_element_is_exist('article:comment'))

        self.article_page.info(
            '+ Check Related article field existance in create page')
        self.assertFalse(self.base_selenium.check_element_is_exist(
            'article:related_article'))

    def test024_user_hide_any_optional_field_in_edit_form(self):
        """
        New: Articles: Optional fields: User can hide/show any optional field in Edit/Create form

        LIMS:4123
        :return:
        """
        # archive the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.archived_optional_fields_flag = True  # to restore the UI in the tearDown

        # open edit page
        self.article_page.get_articles_page()
        self.article_page.info('+ Open article edit')
        self.article_page.get_articles_page()
        self.article_page.open_edit_page(
            row=self.article_page.get_random_article_row())

        self.article_page.info('+ Check Unit field existance in edit page')
        self.assertFalse(
            self.base_selenium.check_element_is_exist('article:unit'))

        self.article_page.info('+ Check Comment field existance in edit page')
        self.assertFalse(
            self.base_selenium.check_element_is_exist('article:comment'))

        self.article_page.info(
            '+ Check Related article field existance in edit page')
        self.assertFalse(self.base_selenium.check_element_is_exist(
            'article:related_article'))

    def test025_user_restore_any_optional_field_is_not_affecting_the_table(self):
        # archive then restore the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.article_page.get_articles_page()
        self.article_page.archive_restore_optional_fields(restore=True)

        # check if the fields still exist in the table after restore
        self.article_page.info('+ Open article table')
        self.article_page.get_articles_page()
        article_headers = self.base_selenium.get_table_head_elements(
            'general:table')
        article_headers_text = [header.text for header in article_headers]

        self.article_page.info('+ Check Comment field existance in the table')
        self.assertIn('Comment', article_headers_text)

        self.article_page.info('+ Check Unit field existance in the table')
        self.assertIn('Unit', article_headers_text)
        # ignore related article since it shouldn't display in the table anyway

    def test026_user_restore_any_optional_field_in_create_form(self):
        # archive then restore the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.article_page.get_articles_page()
        self.article_page.archive_restore_optional_fields(restore=True)

        # open create page after restore
        self.article_page.get_articles_page()
        self.article_page.info('+ Open article create')
        self.base_selenium.click(element='articles:new_article')
        self.article_page.sleep_small()

        self.article_page.info('+ Check Unit field existance in create page')
        self.assertTrue(
            self.base_selenium.check_element_is_exist('article:unit'))

        self.article_page.info(
            '+ Check Comment field existance in create page')
        self.assertTrue(
            self.base_selenium.check_element_is_exist('article:comment'))

        self.article_page.info(
            '+ Check Related article field existance in create page')
        self.assertTrue(self.base_selenium.check_element_is_exist(
            'article:related_article'))

    def test027_user_restore_any_optional_field_in_edit_form(self):
        # archive then restore the optional fields
        self.article_page.archive_restore_optional_fields(restore=False)
        self.article_page.get_articles_page()
        self.article_page.archive_restore_optional_fields(restore=True)

        # open edit page after restore
        self.article_page.get_articles_page()
        self.article_page.info('+ Open article edit')
        self.article_page.get_articles_page()
        self.article_page.open_edit_page(
            row=self.article_page.get_random_article_row())

        self.article_page.info('+ Check Unit field existance in edit page')
        self.assertTrue(
            self.base_selenium.check_element_is_exist('article:unit'))

        self.article_page.info('+ Check Comment field existance in edit page')
        self.assertTrue(
            self.base_selenium.check_element_is_exist('article:comment'))

        self.article_page.info(
            '+ Check Related article field existance in edit page')
        self.assertTrue(self.base_selenium.check_element_is_exist(
            'article:related_article'))

    @parameterized.expand(['name', 'number', 'unit', 'created_at', 'material_type', 'changed_by'])
    def test028_filter_article_by_any_field(self, filter_name):
        """
        New: Article: Filter Approach: I can filter by any static field & and also from the default filter.

        LIMS:3595
        """
        # set default material type and field type
        material_type = 'Raw Material'
        field_type = 'text'
        full_options = False

        # set the material type to None in case of material type filter to test with random material type name
        if filter_name == 'material_type':
            material_type = None

        # change the field type for drop down fields
        if filter_name == 'material_type' or filter_name == 'changed_by':
            field_type = 'drop_down'

        # use full options in case of unit field
        if filter_name == 'unit':
            full_options = True

        # create new article with full options
        article = self.article_page.create_new_article(
            material_type=material_type, full_options=full_options)

        # open article table page and open the filter menu
        self.article_page.get_articles_page()
        self.article_page.sleep_small()
        self.article_page.open_filter_menu()

        # filter the article and get the result
        result_article = self.article_page.filter_article_by(filter_element='article:filter_{}'.format(
            filter_name), filter_text=article[filter_name], field_type=field_type)
        self.assertIn(article[filter_name], result_article.text)

    @parameterized.expand(['name', 'number', 'unit', 'created_at', 'material_type', 'changed_by', 'test_plan'])
    def test029_filter_article_by_any_default_filter(self, filter_name):
        """
        New: Article: Filter Approach: I can filter by any static field & and also from the default filter.

        LIMS:3595
        """
        # set default material type and field type
        material_type = 'Raw Material'
        field_type = 'text'
        full_options = False

        # set the material type to None in case of material type filter to test with random material type name
        if filter_name == 'material_type':
            material_type = None

        # change the field type for drop down fields
        if filter_name == 'material_type' or filter_name == 'changed_by' or filter_name == 'test_plan':
            field_type = 'drop_down'

        # use full options in case of unit field
        if filter_name == 'unit':
            full_options = True

        # create new article with full options
        article = self.article_page.create_new_article(
            material_type=material_type, full_options=full_options)

        # create corresponding test plan
        if filter_name == 'test_plan':
            self.test_plan.get_test_plans_page()
            self.test_plan.create_new_test_plan(
                material_type=article['material_type'], article=article['name'])
            self.article_page.get_articles_page()
            self.article_page.sleep_small()
            article['test_plan'] = self.test_plan.test_plan_name

        # turn on the selected default filters
        self.article_page.toggle_default_filters(
            element1='article:default_filter_{}'.format(filter_name))
        self.default_filters_flags[filter_name] = True

        # filter the article and get the results
        self.article_page.filter_by(
            filter_element='article:filter_{}'.format(filter_name), filter_text=article[filter_name],
            field_type=field_type)
        self.article_page.sleep_medium()
        result_article = self.article_page.result_table()[0]
        self.assertIn(article[filter_name], result_article.text)

    def test028_article_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        articles_response = self.article_api.get_all_articles()
        articles = articles_response[0]['articles']
        article_name = random.choice(articles)['name']
        search_results = self.article_page.search(article_name)
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Article Name'] == article_name:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(article_name, search_data['Article Name'])
        # Navigate to test plan page
        self.article_page.info('navigate to test plans page')
        self.test_plan.get_test_plans_page()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))

    def test030_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        assert (self.article_page.deselect_all_configurations(), False)
