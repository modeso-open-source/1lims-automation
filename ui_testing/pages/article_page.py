from ui_testing.pages.articles_page import Articles
from testconfig import config
from random import randint
import time
from datetime import date


class Article(Articles):
    def create_new_article(self, material_type='', sleep=True, full_options=False):
        self.info(' + Create new article.')
        self.base_selenium.click(element='articles:new_article')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.article_name = self.generate_random_text()
        self.set_name(name=self.article_name)
        if material_type:
            self.set_material_type(material_type)
        else:
            self.set_material_type(random=True)
        self.article_material_type = self.get_material_type()

        self.article_create_date = date.today().strftime("%d.%m.%Y")
        # self.article_create_date = "{}.{}.{}".format(current_date.day, current_date.month, current_date.year)
        self.article_create_user = config['site']['username']

        article_data = {
            "number": self.get_no(),
            "name": self.article_name,
            "material_type": self.article_material_type,
            "created_at": self.article_create_date,
            "changed_at": self.article_create_date,
            "changed_by": self.article_create_user,
            "test_plan": None,
        }

        if full_options:
            self.article_comment = self.generate_random_text()
            self.set_comment(comment=self.article_comment)
            self.article_unit = self.generate_random_text()
            self.set_unit(self.article_unit)
            self.set_related_article()
            self.article_related_article = self.get_related_article()
            article_data = {
                "number": self.get_no(),
                "name": self.article_name,
                "material_type": self.article_material_type,
                "related_article": self.article_related_article,
                "unit": self.article_unit,
                "comment": self.article_comment,
                "created_at": self.article_create_date,
                "changed_at": self.article_create_date,
                "changed_by": self.article_create_user,            
                "test_plan": None,
            }

        self.save()
        self.info(' + Article name : {}'.format(self.article_name))

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

    def filter_article_by(self, filter_element, filter_text, field_type='text'):
        self.info(
            ' + Filter by {} : {}'.format(filter_element.replace('article:filter_', '').replace('_', ' '), filter_text))
        self.filter_by(filter_element=filter_element, filter_text=filter_text, field_type=field_type)
        self.filter_apply()
        self.sleep_tiny()
        return self.base_selenium.get_rows_cells_dict_related_to_header()

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
    
    def toggle_default_filters(self, element1, element2=None):
        self.open_filter_menu()
        self.base_selenium.click(element='general:filter_configuration') # open filter configuration
        self.sleep_small()
        self.base_selenium.click(element=element1)
        if element2:
           self.base_selenium.click(element=element2)
        self.base_selenium.click(element='article:default_filter_save')
        self.sleep_small()
        self.open_filter_menu()
        self.sleep_medium()

    def is_field_active(self, field_name):
        return field_name.lower() in self.base_selenium.get_text('general:configuration_body')

    def is_field_restore(self, field_name):
        return field_name.lower() in self.base_selenium.get_text('general:configuration_body')

    def _archive_field(self, field_name):
        self.base_selenium.click(element='articles:{}_field_options'.format(field_name))
        self.info(' Archive field {}'.format(field_name))
        self.base_selenium.click(element='articles:{}_field_archive'.format(field_name))
        self.confirm_popup()

    def archive_all_optional_fields(self):
        self.info('open article configuration')
        self.open_configuration()
        self._archive_field(field_name='unit')
        self._archive_field(field_name='comment')
        self._archive_field(field_name='related_article')

    def _restore_field(self, field_name):
        self.info(' restore field {}'.format(field_name))
        self.base_selenium.click(element='articles:{}_field_options'.format(field_name))
        self.base_selenium.click(element='articles:{}_field_restore'.format(field_name))
        self.confirm_popup()

    def restore_optional_fields(self):
        self.info('open article configuration')
        self.open_archived_configuration()
        self._restore_field(field_name='unit')
        self._restore_field(field_name='comment')
        self._restore_field(field_name='related_article')

    def filter_and_select(self, article_no):
        self.info("filter by article No {}".format(article_no))
        self.open_filter_menu()
        self.filter_article_by(filter_element='article:filter_number',
                               filter_text=article_no, field_type='text')
        self.close_filter_menu()
        self.sleep_tiny()
        row = self.result_table()[0]
        self.click_check_box(source=row)
        self.sleep_tiny()

