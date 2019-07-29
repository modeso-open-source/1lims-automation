from ui_testing.pages.articles_page import Articles
from random import randint
import time


class Article(Articles):
    def create_new_article(self, material_type='', sleep=True, full_options=False):
        self.base_selenium.LOGGER.info(' + Create new article.')
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

        if full_options:
            self.article_unit = self.generate_random_text()
            self.set_unit(self.article_unit)
            self.set_related_article()
            self.article_related_article = self.get_related_article()
        
        article_data={
            "name": self.article_name,
            "material_type": self.article_material_type
        }

        self.save(sleep)
        self.base_selenium.LOGGER.info(' + Article name : {}'.format(self.article_name))

        return article_data

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
            self.base_selenium.select_item_from_drop_down(element='article:material_type', avoid_duplicate=True)
            return self.get_material_type()
        else:
            self.base_selenium.select_item_from_drop_down(element='article:material_type', item_text=material_type)

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
        self.base_selenium.LOGGER.info(' + Filter by test plan : {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='article:filter_test_plan', filter_text=filter_text)
        self.filter_apply()

    def set_related_article(self):
        self.base_selenium.select_item_from_drop_down(element='article:related_article')

    def get_related_article(self):
        return self.base_selenium.get_text(element='article:related_article').split('\n')[0]

    def set_dynamic_field(self):
        input_items = self.base_selenium.find_element_in_element(source_element='article:field',
                                                                 destination_element='article:field_items')
        for item in input_items:
            label = self.base_selenium.find_element_in_element(source=item, destination_element='general:label')
            if 'select' in label:
                drop_down = self.base_selenium.find_element_in_element(source=item, destination_element='general:drop_down')
                self.base_selenium.select_item_from_drop_down(element_source=drop_down)
            if 'text' in label:
                input_item = self.base_selenium.find_element_in_element(source=item, destination_element='general:input')
                # send text


