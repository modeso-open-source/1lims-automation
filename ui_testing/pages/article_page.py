from ui_testing.pages.articles_page import Articles
from random import randint
import time


class Article(Articles):
    def create_new_article(self, material_type='', sleep=True):
        self.base_selenium.click(element='articles:new_article')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.article_name = self.generate_random_text()
        self.article_comment = self.generate_random_text()
        self.set_name(name=self.article_name)
        self.set_comment(comment=self.article_comment)
        if material_type:
            self.set_material_type(material_type)
        else:
            self.set_material_type(random=True)
        self.article_material_type = self.get_material_type()
        self.save(sleep)

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
        return self.base_selenium.get_text(element='article:material_type').split('\n')[0]

    def set_material_type(self, material_type='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='article:material_type', random=True)
            return self.get_material_type()
        else:
            self.base_selenium.select_item_from_drop_down(element='article:material_type', item_text=material_type, by_text=True)

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

    def filter_by_test_plan(self, filter_text):
        self.filter_by(filter_element='article:filter_test_plan', filter_text=filter_text)
        self.filter_apply()

