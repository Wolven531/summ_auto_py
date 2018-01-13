"""
	This is the EndToEndTests module
"""

import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class EndToEndTests(StaticLiveServerTestCase):
	"""
		This class tests the user facing behavior of the application
	"""
	fixtures = [
		'admin.json',
		'questions.json',
		'monsters.json'
	]
	# NOTE: `serialized_rollback` is required in order to import all of
	# the fixtures with no unique constraint issues (a.k.a. no data integrity issues)
	serialized_rollback = True

	@staticmethod
	def get_screenshot_filepath(app, parent_dir, filename):
		"""
			This method returns the full path of where a given
			screenshot should be saved
		"""
		screenshot_dir = os.path.join(parent_dir, 'screenshots', app)
		return os.path.join(screenshot_dir, filename)

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
			The refresh below is inspired by https://code.djangoproject.com/ticket/21227
		"""
		cls.selenium.refresh()
		cls.selenium.quit()
		super().tearDownClass()

	# @classmethod
	# def setUpTestData(cls):# pylint: disable=C0103
	#	 """
	#		 This method is run before the entire class
	#	 """

	def setUp(self):
		"""
			This method is run before each test
		"""
		curr_dir = os.path.dirname(os.path.abspath(__file__))
		self.parent_dir = os.path.dirname(curr_dir)

	def test_when_question_clicked_should_navigate_to_detail(self):
		"""
			This test ensures the polls index page can be loaded via browser
		"""
		index_screenshot_filepath = EndToEndTests.get_screenshot_filepath(
			'polls',
			self.parent_dir,
			'index.png')
		detail_screenshot_filepath = EndToEndTests.get_screenshot_filepath(
			'polls',
			self.parent_dir,
			'detail.png')

		self.selenium.get(f'{self.live_server_url}/polls/')

		# NOTE: save screenshot of index
		self.selenium.save_screenshot(index_screenshot_filepath)

		question_links = self.selenium.find_elements_by_css_selector('li a')
		self.assertEqual(len(question_links), 1)

		question_links[0].click()
		curr_url = self.selenium.current_url
		self.assertTrue(
			curr_url.endswith('/polls/1/'),
			f'Unexpected URL after clicking Question={curr_url}')

		# NOTE: save screenshot of detail
		self.selenium.save_screenshot(detail_screenshot_filepath)

		choice_inputs = self.selenium.find_elements_by_css_selector('input[type="radio"]')
		self.assertEqual(len(choice_inputs), 2)

	def test_when_monster_clicked_should_navigate_to_detail(self):
		"""
			This test ensures the mons index page can be loaded via browser
		"""
		index_screenshot_filepath = EndToEndTests.get_screenshot_filepath(
			'mons',
			self.parent_dir,
			'index.png')
		detail_screenshot_filepath = EndToEndTests.get_screenshot_filepath(
			'mons',
			self.parent_dir,
			'detail.png')

		self.selenium.get(f'{self.live_server_url}/monsters/')

		# NOTE: save screenshot of index
		self.selenium.save_screenshot(index_screenshot_filepath)

		mon_links = self.selenium.find_elements_by_css_selector('li a')
		self.assertEqual(len(mon_links), 2)

		mon_links[0].click()
		curr_url = self.selenium.current_url
		# NOTE: we expect mon 2 because of the ordering of the mon links
		self.assertTrue(
			curr_url.endswith('/monsters/2/'),
			f'Unexpected URL after clicking Monster={curr_url}')

		# NOTE: save screenshot of detail
		self.selenium.save_screenshot(detail_screenshot_filepath)
