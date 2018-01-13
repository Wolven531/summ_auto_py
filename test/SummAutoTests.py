"""
	This module is used to test functionality of the app
"""
import unittest
import os

from src.LinkType import LinkType
from src.MonsterPage import MonsterPage
from src.MonsterType import MonsterType
from src.PageParser import PageParser
from src.Rating import Rating

class SummAutoTests(unittest.TestCase):
	"""
		This class tests all of the functionality in the SummAuto application
	"""

	@classmethod
	def __validate_mon(cls, target, mon):
		"""
			This method asserts that a MonsterPage object has expected
			values
		"""
		target.assertEqual(
			mon.sleepy_name,
			'Amazon',
			f'Expected monster sleepy name to equal "Amazon"')
		target.assertEqual(
			mon.awaken_name,
			'Mara',
			'Expected monster awakened name to equal "Mara"')

		target.assertEqual(
			mon.element,
			MonsterType.DARK,
			f'Expected monster to be of type {MonsterType.DARK}')

		target.assertEqual(mon.grade, '★★★', 'Expect monster grade to be three stars')
		target.assertEqual(
			mon.grade_num,
			3,
			'Expect numeric value of grade to match number of stars')

		target.assertEqual(mon.mon_type, 'Attack', 'Expect monster type to be "Attack"')
		target.assertEqual(
			mon.get_from,
			'Scroll of Light & Darkness, Temple of Wishes',
			'Expect monster get from to be "Scroll of Light & Darkness, Temple of Wishes"')
		target.assertEqual(
			mon.when_awakened,
			'Leader Skill: The Attack Power of ally Monsters is increased by 21% in Guild Battles.',
			'Inaccurate when awakened message')
		target.assertListEqual(
			mon.good_for,
			['pvp offense against reviver comps'],
			'Inaccurate good for tags')
		target.assertEqual(
			mon.skillup_info,
			'Worth fully skilling up, but use family skill ups instead of Devilmons',
			'Inaccurate skillup info message')

		target.assertAlmostEqual(mon.score_total, 7.7, 3, 'Inaccurate total score')
		target.assertAlmostEqual(mon.score_user, 8.4, 3, 'Inaccurate user score')

		target.assertAlmostEqual(mon.ratings[Rating.KEEP_IT], 40, 3, 'Inaccurate KEEP_IT rating')
		target.assertAlmostEqual(mon.ratings[Rating.FOOD], 4, 3, 'Inaccurate FOOD rating')
		target.assertAlmostEqual(mon.ratings[Rating.THE_BEST], 53, 3, 'Inaccurate THE_BEST rating')
		target.assertAlmostEqual(mon.ratings[Rating.MEH], 3, 3, 'Inaccurate MEH rating')

		target.assertTrue(
			mon.links[LinkType.IMAGE_SLEEPY].endswith('Amazon_Dark_Icon.png'),
			f'Inaccurate link for {LinkType.IMAGE_SLEEPY}={mon.links[LinkType.IMAGE_SLEEPY]}'
		)
		target.assertTrue(
			mon.links[LinkType.IMAGE_AWAKE].endswith('Mara_Icon.png'),
			f'Inaccurate link for {LinkType.IMAGE_AWAKE}={mon.links[LinkType.IMAGE_AWAKE]}'
		)

		target.assertEqual(
			mon.links[LinkType.FIRE],
			'//summonerswar.co/fire-amazon-ceres/',
			f'Inaccurate link for {LinkType.FIRE}')
		target.assertEqual(
			mon.links[LinkType.WATER],
			'//summonerswar.co/water-amazon-ellin/',
			f'Inaccurate link for {LinkType.WATER}')
		target.assertEqual(
			mon.links[LinkType.WIND],
			'//summonerswar.co/wind-amazon-hina/',
			f'Inaccurate link for {LinkType.WIND}')
		target.assertEqual(
			mon.links[LinkType.LIGHT],
			'//summonerswar.co/light-amazon-lyn/',
			f'Inaccurate link for {LinkType.LIGHT}')
		target.assertEqual(
			mon.links[LinkType.DARK],
			'//summonerswar.co/dark-amazon-mara/',
			f'Inaccurate link for {LinkType.DARK}')

	@unittest.skip('Skipping searched_link load unless manually enabled...')
	def test_parse_search_pages(self):
		"""
			Make sure we can hit the landing page which contains
			all of the monster in default sorting
		"""
		info = PageParser.parse_search_pages()
		self.assertEqual(
			info['count'],
			PageParser.TOTAL_MON_COUNT,
			f'Expected {PageParser.TOTAL_MON_COUNT} hrefs...')

	def test_get_filepath(self):
		"""
			Make sure the filepath is safe and looks good
		"""
		mon = PageParser.ensure_mon_load('https://summonerswar.co/dark-amazon-mara/')
		actual = mon.get_filepath()
		self.assertTrue(
			actual.endswith('dark_amazon_mara.json'),
			f'Incorrect filepath. Got "{actual}"')

	def test_serialization(self):
		"""
			Make sure we can write to disk so we do not need
			to scrape every time
		"""
		mon = PageParser.ensure_mon_load('https://summonerswar.co/dark-amazon-mara/')
		mon.serialize()
		filepath = mon.get_filepath()
		self.assertTrue(
			os.path.isfile(filepath),
			f'Expected to find serialized MonsterPage at {filepath}')

	def test_deserialization(self):
		"""
			Make sure we can read from disk so we do not need
			to scrape every time
		"""
		mon = PageParser.ensure_mon_load('https://summonerswar.co/dark-amazon-mara/')
		mon.serialize()
		filepath = mon.get_filepath()
		new_mon = MonsterPage.load_from_disk(filepath)
		self.__validate_mon(self, new_mon)

	def test_parse_single_mon_page(self):
		"""
			Make sure we can load and parse information from
			a single monster page
		"""
		mon = PageParser.ensure_mon_load('https://summonerswar.co/dark-amazon-mara/')
		# mon.print_mon_info()
		self.__validate_mon(self, mon)

if __name__ == '__main__':
	unittest.main()
