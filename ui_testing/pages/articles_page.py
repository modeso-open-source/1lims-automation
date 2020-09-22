from ui_testing.pages.base_pages import BasePages
from random import randint


class Articles(BasePages):
    def __init__(self):
        super().__init__()
        self.article_url = "{}articles".format(self.base_selenium.url)

    def get_articles_page(self):
        self.base_selenium.get(url=self.article_url)
        self.wait_until_page_is_loaded()

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
        row = self.get_random_article_row()
        self.open_edit_page(row=row)

    def get_random_article_row(self):
        return self.get_random_table_row(table_element='articles:article_table')
        
    def archive_selected_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:archive')
        self.confirm_popup()
        self.sleep_tiny()

    def restore_selected_articles(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:restore')
        self.confirm_popup()
        self.sleep_tiny()


    def is_article_in_table(self, value):
        """
            - get_archived_articles then call me to check if the article has been archived.
            - get_active_articles then call me to check if the article is active.
        :param value: search value
        :return:
        """
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

    def delete_selected_article(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:delete')
        #self.confirm_popup()

        if self.base_selenium.check_element_is_exist(element='general:cant_delete_message'):
            self.base_selenium.click(element='general:confirm_pop')
            return False
        return True

    def get_article_edit_page_by_id(self, id):
        url_text = "{}sample/articles/" + str(id)
        self.base_selenium.get(url=url_text.format(self.base_selenium.url))
        self.wait_until_page_is_loaded()

