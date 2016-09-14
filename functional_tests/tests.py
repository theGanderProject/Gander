from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from django.contrib.auth.models import User

class UserCanSubmitLiterature(StaticLiveServerTestCase):

    def setUp(self):
        user = User.objects.create_user('user', password='password')
        user.save()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_submit_writing(self):
        # John wants to submit a story
        self.browser.get(self.live_server_url + '/writing/submit/')

        # John is not logged in, so he's redirected to the login page
        self.assertIn(self.browser.current_url, '/login/')

        input = self.browser.find_element_by_id("id_username")
        input.send_keys('user')
        input = self.browser.find_element_by_id("id_password")
        input.send_keys('password')
        input.submit()

        # John is then redirected to the submit page
        self.assertEqual(self.browser.current_url, self.live_server_url + '/writing/submit/')

        # John then enters text into the textbox
        input = self.browser.find_element_by_id("id_editor")
        input.send_keys('This is my story.')

        # John then navigates away without saving
        time.sleep(6)
        self.browser.get(self.live_server_url + '/')

        # John returns
        self.browser.get(self.live_server_url + '/writing/submit/')

        # John sees that his story is still in the textbox
        text = self.browser.find_element_by_id("id_editor")
        time.sleep(6)
        # need to finish the test

class CreateAccountAndLogin(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_account(self):
        self.browser.get(self.live_server_url + '/accounts/register/')
        input = self.browser.find_element_by_id("id_username")
        input.send_keys('user')
        input = self.browser.find_element_by_id("id_password1")
        input.send_keys('w24gwois42rfs')
        input = self.browser.find_element_by_id("id_password2")
        input.send_keys('w24gwois42rfs')
        input.submit()

        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/success/')


class UserUploadsToTheirGallery(StaticLiveServerTestCase):

    def setUp(self):
        user = User.objects.create_user('user', password='password')
        user.save()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()

    def test_can_upload_image(self):
        # John wants to upload an image
        # He starts on the home page and sees that there's no images
        self.browser.get(self.live_server_url)

        images = self.browser.find_elements_by_tag_name('img')
        self.assertEqual(0, len(images))

        # He goes to the image upload page
        # But he's not logged in, so he's redirected to the login page
        self.browser.get(self.live_server_url + '/art/submit/')
        input = self.browser.find_element_by_id("id_username")
        input.send_keys('user')
        input = self.browser.find_element_by_id("id_password")
        input.send_keys('password')
        input.submit()

        # upon logging in, he's diredrected to the image upload page
        # where he sees a form for uploading images
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/art/submit/')

        # He uploads an image and is automatically redirected to the
        # home page, where he sees his image
        input = self.browser.find_element_by_id("id_original")
        input.send_keys(os.getcwd() + '/media_for_tests/testImage1.jpg')
        input = self.browser.find_element_by_id("id_title")
        input.send_keys('title')
        input = self.browser.find_element_by_id("id_description")
        input.send_keys('description')
        input.submit()
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/')
        images = self.browser.find_elements_by_tag_name('img') #change later
        self.assertEqual(1, len(images))

        # He then clicks on the image to see detailed information about id_title
        link = self.browser.find_element_by_tag_name('a')
        link.click()

        # He sees the title and description of the image
        #self.assertIn('title', self.browser.body)
        #self.assertIn('description', self.browser.body)
        self.fail('Finish the test!')

        # He also sees the full image