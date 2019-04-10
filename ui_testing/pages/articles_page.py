from ui_testing.pages.base_pages import BasePages
from random import randint


class Articles(BasePages):
    def __init__(self):
        super().__init__()
        self.article_url = "{}articles".format(self.base_selenium.url)

    def get_article_page(self):
        self.base_selenium.get(url=self.article_url)

    def archive_article(self, name='', random=False, force=True):
        if not random:
            article = self.search(value=name)[0]
            if article is not None:
                article_archive_button = self.base_selenium.find_element_in_element(source=article,
                                                                                    destination_element='articles:article_archive_button')
                article_archive_button.click()
                self.base_selenium.click(element='articles:article_archive_dropdown')
                if force:
                    self.base_selenium.click(element='articles:confirm_archive')
                else:
                    self.base_selenium.click(element='articles:cancel_archive')
                self.sleep_medium()

    def get_random_article(self):
        row = self.base_selenium.get_table_rows(element='articles:article_table')
        row_id = randint(1, len(row) - 1)
        row = row[row_id]
        article_edit_button = self.base_selenium.find_element_in_element(source=row,
                                                                         destination_element='articles:article_edit_button')
        article_edit_button.click()
        self.sleep_medium()

