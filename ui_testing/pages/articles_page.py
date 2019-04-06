from ui_testing.pages.base_selenium import BaseSelenium
from ui_testing.pages.base_pages import BasePages
from random import randint
import time


class Articles(BasePages):
    def __init__(self):
        super().__init__()
        self.article_url = "{}articles".format(self.base_selenium.url)

    def get_article_page(self):
        self.base_selenium.get(url=self.article_url)

    def get_random_article(self):
        row = self.base_selenium.get_table_rows(element='articles:article_table')
        row_id = randint(1, len(row) - 1)
        row= row[row_id]
        article_edit_button = self.base_selenium.find_element_in_element(source=row, destination_element='articles:article_edit_button')
        article_edit_button.click()
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def create_new_article(self):
        self.base_selenium.click(element='articles:new_article')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.article_name = self.generate_random_text()
        self.article_comment = self.generate_random_text()
        self.set_name(name=self.article_name)
        self.set_comment(comment=self.article_comment)
        self.set_material_type(random=True)
        self.article_material_type = self.get_material_type()
        self.save()

    def archive_article(self, name='', random=False, force=True):
        if not random:
            article = self.search(value=name)
            if article is not None:
                article_archive_button = self.base_selenium.find_element_in_element(source=article,
                                                                                    destination_element='articles:article_archive_button')
                article_archive_button.click()
                self.base_selenium.click(element='articles:article_archive_dropdown')
                if force:
                    self.base_selenium.click(element='articles:confirm_archive')
                else:
                    self.base_selenium.click(element='articles:cancel_archive')
                time.sleep(self.base_selenium.TIME_MEDIUM)

    def edit_random_article(self, edit_method, edit_value, save=True):
        if 'unit' in edit_method:
            self.set_unit(edit_value)
        elif 'no' in edit_method:
            self.set_no(edit_value)
        elif 'name' in edit_method:
            self.set_name(edit_value)
        elif 'comment' in edit_method:
            self.set_comment(edit_value)

        if save:
            self.save()
        else:
            self.cancel()

    def get_unit(self):
        return self.base_selenium.get_value(element="article:unit")

    def set_unit(self, unit):
        self.base_selenium.set_text(element="article:unit", value=unit)

    def get_material_type(self):
        return self.base_selenium.get_text(element='article:material_type')

    def set_material_type(self, data='', random=False):
        if random:
            self.base_selenium.click(element='article:material_type')
            self.base_selenium.select_random_item('article:material_type_options')
        else:
            self.base_selenium.set_text(element='article:material_type', value=data)

    def get_no(self):
        return self.base_selenium.get_value(element="article:no")

    def set_no(self, no):
        self.base_selenium.set_text(element="article:no", value=no)

    def get_name(self):
        return self.base_selenium.get_value(element="article:name")

    def set_name(self, name):
        self.base_selenium.set_text(element="article:name", value=name)

    def get_comment(self):
        return self.base_selenium.get_value(element="article:comment")

    def set_comment(self, comment):
        self.base_selenium.set_text(element="article:comment", value=comment)

    def save(self):
        self.base_selenium.click(element='article:save')
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def cancel(self, force=True):
        self.base_selenium.click(element='article:cancel')
        if self.base_selenium.check_element_is_exist(element='article:confirmation_pop_up'):
            if force:
                self.base_selenium.click(element='article:confirm_pop')
            else:
                self.base_selenium.click(element='article:confirm_cancel')
        time.sleep(self.base_selenium.TIME_MEDIUM)
