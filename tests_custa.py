from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import os, socket

from django.contrib.staticfiles import finders

import population_script
from custa_falcon_x import settings


class CustaTests(TestCase):

    # Check the index template
    def test_index_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'custa/index.html')

    # Check if index page contains title
    def test_index_contains_title(self):
        response = self.client.get(reverse('index'))
        self.assertIn('Your gateway to custom pasta'.lower(), response.content.decode('ascii').lower())

    # Check if there is a base template used
    def test_base_template_exists(self):
        path_to_base = settings.TEMPLATE_DIR + '/custa/base.html'
        print(path_to_base)
        self.assertTrue(os.path.isfile(path_to_base))

    # Check if logo picture is present on the page
    def test_card1_picture_displayed(self):
        response = self.client.get(reverse('index'))
        self.assertIn("img class=\"cardimg\" src=\"/static/assets/custa-card1.jpg\"".lower(), response.content.decode('ascii').lower())

    # Check the url references on the index page when not logged in
    def test_displayed_url_references_logged_out(self):
        response = self.client.get(reverse('index'))

        self.assertIn(reverse('index'), response.content.decode('ascii'))
        self.assertIn(reverse('contact'), response.content.decode('ascii'))
        self.assertIn(reverse('login'), response.content.decode('ascii'))
        self.assertIn(reverse('register'), response.content.decode('ascii'))

    # Check the url references on the index page when logged in
    def test_displayed_url_references_logged_in(self):
        from custa.models import User, UserProfile
        user = User.objects.get_or_create(username="testuser", password="testpassword",email= "testuser@test.com")[0]
        userprofile = UserProfile.objects.get_or_create(user=user,  phone="07678453459", address="100 University Avenue")[0]
        user.set_password(user.password)
        user.save()
        userprofile.save()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))

        self.assertIn(reverse('index'), response.content.decode('ascii'))
        self.assertIn(reverse('contact'), response.content.decode('ascii'))
        self.assertIn(reverse('order'), response.content.decode('ascii'))
        self.assertIn(reverse('custamise'), response.content.decode('ascii'))
        self.assertIn(reverse('my-account'), response.content.decode('ascii'))


    # Check restricted CUSTAmise page
    def test_CUSTAmise_restricted(self):
        from custa.models import User, UserProfile
        user = User.objects.get_or_create(username="testuser", password="testpassword", email="testuser@test.com")[0]
        userprofile = UserProfile.objects.get_or_create(user=user, phone="07678453459", address="100 University Avenue")[0]
        user.set_password(user.password)
        user.save()
        userprofile.save()

        self.client.login(username='testuser', password='testpassword')

        # Access restricted CUSTAmise page and check title
        response = self.client.get(reverse('custamise'))
        self.assertIn("custamise".lower(), response.content.decode('utf-8').lower())


class CustaLiveServerTests(StaticLiveServerTestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("test-type")
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(CustaLiveServerTests, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    # Check the navigation from the home page to the Contact page
    def test_navigate_from_index_to_contact(self):
        # Go to index page
        self.client.get(reverse('index'))
        url = self.live_server_url

        self.browser.get(url + reverse('index'))
        print(self.browser.current_url)
        self.browser.set_window_size(1920, 1080)
        # Search for the link to Contact page
        contact_nav = self.browser.find_element_by_id('nav-contact')
        contact_link = self.browser.find_element_by_id('contact-link')
        ActionChains(self.browser).move_to_element(contact_nav).click(contact_link).perform()
        print(self.browser.current_url)

        # Check if it returns to the contact page
        self.assertIn(url + reverse('contact'), self.browser.current_url)

    # Check the navigation from the contact page to the login page
    def test_navigate_from_contact_to_login(self):
        # Go to contact page
        self.client.get(reverse('index'))
        url = self.live_server_url

        self.browser.get(url + reverse('contact'))
        print(self.browser.current_url)
        self.browser.set_window_size(1920, 1080)
        # Search for the link to index page
        index_nav = self.browser.find_element_by_id('nav-index')
        index_link = self.browser.find_element_by_id('index-link')
        ActionChains(self.browser).move_to_element(index_nav).click(index_link).perform()
        print(self.browser.current_url)

        # Check if it returns to the contact page
        self.assertIn(url + reverse('index'), self.browser.current_url)

    # Check population script with bases
    def test_population_script(self):
         # Populate database
         population_script.populate()
         url = self.live_server_url
         url = url.replace('localhost', '127.0.0.1')
         self.browser.get(url + reverse('admin:index'))


         username_field = self.browser.find_element_by_name('username')
         username_field.send_keys('admin')

         password_field = self.browser.find_element_by_name('password')
         password_field.send_keys('admin')
         password_field.send_keys(Keys.RETURN)

         # # Check if there is a link to bases
         # bases_link = self.browser.find_elements_by_partial_link_text('bases')
         # print(bases_link[0].text)
         # bases_link[0].click()

         # Check for the bases
         self.browser.find_elements_by_partial_link_text('Bases')[0].click()
         self.browser.find_elements_by_partial_link_text('Fusilli')
         self.browser.find_elements_by_partial_link_text('Spaghetti')
         self.browser.find_elements_by_partial_link_text('Tortellini')
         self.browser.find_elements_by_partial_link_text('Macaroni')
         self.browser.find_elements_by_partial_link_text('Egg Noodles')
