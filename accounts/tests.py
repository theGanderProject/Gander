from django.test import TestCase
from django.core.urlresolvers import resolve

# Create your tests here.
class LoginTest(TestCase):
    #if get 200, success
    def test_get_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

class LogoutTest(TestCase):

    def test_get_logout_page(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

class PasswordChangeTest(TestCase):

    def test_get_redirected_to_login_page_when_not_logged_in(self):
        response = self.client.get('/accounts/password_change/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/password_change/')


class PasswordResetTest(TestCase):

    def test_get_password_reset_page(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)