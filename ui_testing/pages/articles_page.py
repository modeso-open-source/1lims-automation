from ui_testing.pages.base_pages import BasePages
from random import randint


class Articles(BasePages):
    def __init__(self):
        super().__init__()
        self.article_url = "{}articles".format(self.base_selenium.url)

    def get_article_page(self):
        self.base_selenium.get(url=self.article_url)
        self.sleep_small()

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

    def archive_selected_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:archive')
        self.confirm_popup()

    def restore_selected_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:restore')
        self.confirm_popup()

    def is_article_archived(self, value):
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def get_archived_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:archived')
        self.sleep_small()

    def get_active_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:active')
        self.sleep_small()
