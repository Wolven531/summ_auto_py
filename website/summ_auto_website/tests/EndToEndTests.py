"""
    This is the EndToEndTests module
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class EndToEndTests(StaticLiveServerTestCase):
    """
        This class tests the user facing behavior of the application
    """
    fixtures = ['questions.json']

    @classmethod
    def setUpClass(cls):
        """
            This method runs during setup for setup purposes
        """
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        # cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """
            This method runs during teardown for cleanup purposes
        """
        cls.selenium.quit()
        super().tearDownClass()

    # @classmethod
    # def setUpTestData(cls):# pylint: disable=C0103
    #     """
    #         This method is run before the entire class
    #     """

    # def setUp(self):
    #     """
    #         This method is run before each test
    #     """

    def test_when_question_clicked_should_navigate_to_detail(self):
        """
            This test ensures the polls index page can be loaded via browser
        """
        self.selenium.get(f'{self.live_server_url}/polls/')

        question_links = self.selenium.find_elements_by_css_selector('li a')
        self.assertEqual(len(question_links), 1)

        question_links[0].click()
        curr_url = self.selenium.current_url
        self.assertTrue(
            curr_url.endswith('/polls/1/'),
            f'Unexpected URL after clicking Question={curr_url}')

        choice_inputs = self.selenium.find_elements_by_css_selector('input[type="radio"]')
        self.assertEqual(len(choice_inputs), 2)
