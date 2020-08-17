# from ui_testing.testcases.base_test import BaseTest
# from ui_testing.pages.login_page import Login
# from parameterized import parameterized
# import time
#
#
# class LoginTestCases(BaseTest):
#     def setUp(self):
#         super().setUp()
#         self.login_page = Login()
#
#     def test001_login_correct_data(self):
#         """
#         Login with valid data
#         :return:
#         """
#         self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
#         time.sleep(15)
#         self.assertIn('dashboard', self.login_page.base_selenium.get_url())
#
#     @parameterized.expand([
#         ('admin', ''),
#         ('', 'admin'),
#         ('', ''),
#         (147852963, 147852963),
#         ('#!@#!@#', '#!@#!@#!@'),
#         ("' 1==1 &", "' 1==1 &")
#     ])
#     def test002_login_incorrect_data(self, username, password):
#         """
#         Login with non-valid data
#         :param username:
#         :param password:
#         :return:
#         """
#         self.login_page.login(username=username, password=password)
#         time.sleep(5)
#         self.assertIn('login', self.login_page.base_selenium.get_url())
