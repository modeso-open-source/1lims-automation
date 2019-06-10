from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.order_page import Order
from parameterized import parameterized
import re


class ArticlesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Article()
        self.test_plan = TstPlan()
        self.order = Order()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.article_page.get_article_page()

    @parameterized.expand(['save', 'cancel'])
    def test002_cancel_button_edit_unit(self, save):
        """
        New: Article: Save/Cancel button: After I edit unit field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_unit = self.article_page.get_unit()
        new_unit = self.generate_random_string()
        self.article_page.set_unit(new_unit)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

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
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_no = self.article_page.get_no()
        new_no = self.generate_random_string()
        self.article_page.set_no(new_no)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

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
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()

        current_name = self.article_page.get_name()
        new_name = self.generate_random_string()
        self.article_page.set_name(new_name)

        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

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
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        current_comment = self.article_page.get_comment()
        new_comment = self.generate_random_string()
        self.article_page.set_comment(new_comment)
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=article_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_comment, self.article_page.get_comment())
        else:
            self.assertEqual(current_comment, self.article_page.get_comment())

    @parameterized.expand(['save', 'cancel'])
    def test006_cancel_button_edit_material_type(self, save):
        """
        New: Article: Save/Cancel button: After I edit material_type then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.article_page.get_random_article()
        article_url = self.base_selenium.get_url()
        self.article_page.sleep_tiny()
        current_material_type = self.article_page.get_material_type()
        self.article_page.set_material_type(random=True)
        new_material_type = self.article_page.get_material_type()
        if 'save' == save:
            self.article_page.save()
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=article_url, sleep=5)

        if 'save' == save:
            self.assertEqual(new_material_type, self.article_page.get_material_type())
        else:
            self.assertEqual(current_material_type, self.article_page.get_material_type())

    def test007_archived_articles_shoudnt_dispaly_in_test_plan(self):
        """
        New: Article: In case I archived any article this article shouldn't display in the test plan module when
         I create test plan or edit it
         
         LIMS-3668
        :return: 
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.article_page.archive_article(name=self.article_page.article_name)
        self.test_plan.get_test_plans_page()
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type=self.article_page.article_material_type)
        self.article_page.sleep_tiny()
        self.assertFalse(self.test_plan.is_article_existing(article=self.article_page.article_name))

    def test008_archived_articles_shoudnt_dispaly_in_order(self):
        """
        New: Article: Archived any article this article shouldn't display in the order module

         LIMS-3668
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.article_page.archive_article(name=self.article_page.article_name)
        self.order.get_orders_page()
        self.order.click_create_order_button()
        self.order.set_new_order()
        self.order.set_material_type(material_type=self.article_page.article_material_type)
        self.article_page.sleep_tiny()
        self.assertFalse(self.order.is_article_existing(article=self.article_page.article_name))

    def test009_created_article_appear_in_test_plan(self):
        """
            New: Article/Test plan: Any article I created should appear in the test plan according to the materiel type.

            LIMS-3581
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type=self.article_page.article_material_type)
        self.article_page.sleep_tiny()
        self.assertTrue(self.test_plan.is_article_existing(article=self.article_page.article_name))

    def test010_create_article_with_test_plan_search_by_test_plan(self):
        """
        In case I create test plan with the article that I created, this test plan should display in the table view

        LIMS-3583
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name)
        self.article_page.get_article_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=self.test_plan.test_plan_name)[0]
        self.assertIn(self.test_plan.test_plan_name, article.text)

        self.test_plan.get_test_plans_page()
        self.test_plan.get_test_plan_edit_page(name=self.test_plan.test_plan_name)

        self.test_plan.clear_article()
        self.test_plan.set_article(article='All')
        self.test_plan.save()
        self.article_page.get_article_page()
        article = self.article_page.search(self.article_page.article_name)[0]
        self.assertNotIn(self.test_plan.test_plan_name, article.text)

    def test011_create_article_with_test_plan_filter_by_test_plan(self):
        """
        In case I create test plan with the article that I created, user could filter with test plan

        LIMS-3583
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name)
        self.article_page.get_article_page()
        self.article_page.sleep_small()

        self.article_page.filter_by_test_plan(filter_text=self.test_plan.test_plan_name)
        article = self.article_page.filter_result()[0]
        self.assertIn(self.test_plan.test_plan_name, article.text)

    def test012_archive_articles(self):
        """
        New: Article: Archive Approach: I can archive/restore any article successfully

        LIMS-3587
        :return:
        """
        selected_articles, _ = self.article_page.select_random_multiple_table_rows()
        self.article_page.archive_selected_articles()
        self.article_page.get_archived_articles()
        for article in selected_articles:
            article_name = article.split('\n')[-4]
            self.assertTrue(self.article_page.is_article_archived(value=article_name))

    def test013_restore_articles(self):
        """
        New: Article: Restore Approach: I can archive/restore any article successfully

        LIMS-3587
        :return:
        """
        article_names = []
        self.article_page.get_archived_articles()
        selected_articles, selected_rows = self.article_page.select_random_multiple_table_rows()
        for article in selected_rows:
            article_names.append(self.article_page.get_row_cell_text_related_to_header(row=article,
                                                                                       column_value='Article Name'))

        self.article_page.restore_selected_items()
        self.article_page.get_active_articles()
        for article_name in article_names:
            self.assertTrue(self.article_page.is_article_archived(value=article_name))

    def test014_create_new_material_type(self):
        """
        Article: Materiel type Approach: make sure you can create new materiel type & this materiel type displayed correct according to this article.
        
        LIMS-3582
        :return: 
        """
        material_type = self.generate_random_string()
        self.article_page.create_new_article(material_type=material_type)
        self.test_plan.get_test_plans_page()
        self.test_plan.click_create_test_plan_button()
        self.test_plan.set_material_type(material_type=self.article_page.article_material_type)
        self.article_page.sleep_tiny()
        self.assertTrue(self.test_plan.is_article_existing(article=self.article_page.article_name))

    def test015_article_search(self):
        """
        New: Articles: Search Approach: I can search by any field in the table view

        LIMS-3594
        :return:
        """
        row = self.article_page.get_random_article_row()
        row_text = row.text
        for row_text_item in row_text.split('\n'):
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_text_item):
                continue
            tmp_row = self.article_page.search(row_text_item)[0].text
            self.assertEqual(tmp_row, row_text)

    def test016_green_border(self):
        """
        New: All modules: Creation Approach: Green border displayed when I create new record

        LIMS-3597
        :return:
        """
        self.article_page.create_new_article(sleep=False, material_type='Raw Material')
        self.assertEqual(self.base_selenium.get_text(element='articles:alert_confirmation'), 'Successfully created')

    def test017_create_full_options_article(self):
        """
        New: Articles: Creation Approach: I can create new article successfully

        LIMS-3575
        :return:
        """
        self.article_page.create_new_article(full_options=True, material_type='Raw Material')
        article_text = self.article_page.search(value=self.article_page.article_name)[0].text
        self.assertIn(self.article_page.article_unit, article_text)
        self.assertIn(self.article_page.article_comment, article_text)
        self.assertIn(self.article_page.article_material_type, article_text)

    def test018_delete_article_with_test_plan(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name)
        self.article_page.get_article_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=self.test_plan.test_plan_name)[0]

        self.article_page.click_check_box(source=article)
        self.article_page.archive_selected_articles()

        self.article_page.get_archived_articles()
        archived_article = self.article_page.search(value=self.test_plan.test_plan_name)[0]
        self.article_page.click_check_box(source=archived_article)
        self.assertFalse(self.article_page.delete_selected_article())

    def test019_delete_article_with_order(self):
        """
        New: Articles: Delete Approach; I can't delete any article if this article related to some data

        LIMS-3577
        :return:
        """
        self.article_page.create_new_article(material_type='Raw Material')
        self.test_plan.get_test_plans_page()
        self.test_plan.create_new_test_plan(material_type=self.article_page.article_material_type,
                                            article=self.article_page.article_name,
                                            test_unit='Qualitative')
        self.order.get_orders_page()
        self.order.click_create_order_button()
        self.order.create_new_order(article=self.article_page.article_name,
                                    material_type=self.article_page.article_material_type,
                                    test_plan=self.test_plan.test_plan_name)

        self.article_page.get_article_page()
        self.article_page.sleep_small()
        article = self.article_page.search(value=self.test_plan.test_plan_name)[0]

        self.article_page.click_check_box(source=article)
        self.article_page.archive_selected_articles()

        self.article_page.get_archived_articles()
        archived_article = self.article_page.search(value=self.test_plan.test_plan_name)[0]
        self.article_page.click_check_box(source=archived_article)
        self.assertFalse(self.article_page.delete_selected_article())

    def test020_download_article_sheet(self):
        """
        New: Articles: XSLX File: I can download all the data in the table view in the excel sheet

        LIMS:3589
        :return:
        """
        self.article_page.download_xslx_sheet()
        rows_data = self.article_page.get_articles_rows_data()
        for index in range(len(rows_data)):
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.article_page.article_sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)


