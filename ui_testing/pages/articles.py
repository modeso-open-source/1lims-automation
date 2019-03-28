from ui_testing.pages.base_selenium import BaseSelenium
from random import randint


class Articles:
    def __init__(self):
        self.base_selenium = BaseSelenium()
        self.article_url = "{}articles".format(self.base_selenium.url)

    def get_article_page(self):
        self.base_selenium.get(url=self.article_url)

    def get_random_article(self):
        self.rows = self.base_selenium.get_table_rows(element='article_table')
        self.row_id = randint(1, len(self.rows) - 1)
        self.row = self.rows[self.row_id]
        article_edit_button = self.base_selenium.find_element_in_element(source=self.row, destination_element='article_edit_button')
        article_edit_button.click()

    def edit_random_article(self, edit_method, edit_value, save=True):
        if 'unit' in edit_method:
            self.edit_unit(edit_value)
        elif 'no' in edit_method:
            self.edit_no(edit_value)
        elif 'name' in edit_method:
            self.edit_name(edit_value)
        elif 'comment' in edit_method:
            self.edit_comment(edit_value)

        if save:
            self.save_edit()
        else:
            self.cancel_edit()

    def get_unit(self):
        return self.base_selenium.get_text(element="unit")

    def edit_unit(self, unit):
        self.base_selenium.set_text(element="unit", value=unit)

    def get_no(self):
        return self.base_selenium.get_value(element="no")

    def edit_no(self, no):
        self.base_selenium.set_text(element="no", value=no)

    def get_name(self):
        return self.base_selenium.get_text(element="name")

    def edit_name(self, name):
        self.base_selenium.set_text(element="name", value=name)

    def get_comment(self):
        return self.base_selenium.get_value(element="comment")

    def edit_comment(self, comment):
        self.base_selenium.set_text(element="comment", value=comment)

    def save_edit(self):
        self.base_selenium.click(element='save')

    def cancel_edit(self, force=True):
        self.base_selenium.click(element='cancel')
        if self.base_selenium.check_element_is_exist(element='confirmation_pop_up'):
            if force:
                self.base_selenium.click(element='confirm_pop')
            else:
                self.base_selenium.click(element='confirm_cancel')
