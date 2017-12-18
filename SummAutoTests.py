"""
    This module is used to test functionality of the app
"""

import unittest

import os

from LinkType import LinkType
from MonsterType import MonsterType
from PageParser import PageParser
from Rating import Rating

class SummAutoTests(unittest.TestCase):
    """
        This class tests all of the functionality in the SummAuto application
    """

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

    def test_parse_single_mon_page(self):
        """
            Make sure we can load and parse information from
            a single monster page
        """
        mon = PageParser.ensure_mon_load('https://summonerswar.co/dark-amazon-mara/')
        # mon.print_mon_info()

        self.assertEqual(
            mon.sleepy_name,
            'Amazon',
            f'Expected monster sleepy name to equal "Amazon"')
        self.assertEqual(
            mon.awaken_name,
            'Mara',
            'Expected monster awakened name to equal "Mara"')

        self.assertEqual(
            mon.element,
            MonsterType.DARK,
            f'Expected monster to be of type {MonsterType.DARK}')

        self.assertEqual(mon.grade, '★★★', 'Expect monster grade to be three stars')
        self.assertEqual(
            mon.grade_num,
            3,
            'Expect numeric value of grade to match number of stars')

        self.assertEqual(mon.mon_type, 'Attack', 'Expect monster type to be "Attack"')
        self.assertEqual(
            mon.get_from,
            'Scroll of Light & Darkness, Temple of Wishes',
            'Expect monster get from to be "Scroll of Light & Darkness, Temple of Wishes"')
        self.assertEqual(
            mon.when_awakened,
            'Leader Skill: The Attack Power of ally Monsters is increased by 21% in Guild Battles.',
            'Inaccurate when awakened message')
        self.assertEqual(
            mon.good_for,
            'PvP Offense against reviver comps',
            'Inaccurate good for message')
        self.assertEqual(
            mon.skillup_info,
            'Worth fully skilling up, but use family skill ups instead of Devilmons',
            'Inaccurate skillup info message')

        self.assertAlmostEqual(mon.score_total, 7.7, 3, 'Inaccurate total score')
        self.assertAlmostEqual(mon.score_user, 8.4, 3, 'Inaccurate user score')

        self.assertAlmostEqual(mon.ratings[Rating.KEEP_IT], 39, 3, 'Inaccurate KEEP_IT rating')
        self.assertAlmostEqual(mon.ratings[Rating.FOOD], 4, 3, 'Inaccurate FOOD rating')
        self.assertAlmostEqual(mon.ratings[Rating.THE_BEST], 54, 3, 'Inaccurate THE_BEST rating')
        self.assertAlmostEqual(mon.ratings[Rating.MEH], 2, 3, 'Inaccurate MEH rating')

        self.assertTrue(
            mon.links[LinkType.IMAGE_SLEEPY].endswith('Amazon_Dark_Icon.png'),
            f'Inaccurate link for {LinkType.IMAGE_SLEEPY}={mon.links[LinkType.IMAGE_SLEEPY]}'
        )
        self.assertTrue(
            mon.links[LinkType.IMAGE_AWAKE].endswith('Mara_Icon.png'),
            f'Inaccurate link for {LinkType.IMAGE_AWAKE}={mon.links[LinkType.IMAGE_AWAKE]}'
        )

        self.assertEqual(
            mon.links[LinkType.FIRE],
            '//summonerswar.co/fire-amazon-ceres/',
            f'Inaccurate link for {LinkType.FIRE}')
        self.assertEqual(
            mon.links[LinkType.WATER],
            '//summonerswar.co/water-amazon-ellin/',
            f'Inaccurate link for {LinkType.WATER}')
        self.assertEqual(
            mon.links[LinkType.WIND],
            '//summonerswar.co/wind-amazon-hina/',
            f'Inaccurate link for {LinkType.WIND}')
        self.assertEqual(
            mon.links[LinkType.LIGHT],
            '//summonerswar.co/light-amazon-lyn/',
            f'Inaccurate link for {LinkType.LIGHT}')
        self.assertEqual(
            mon.links[LinkType.DARK],
            '//summonerswar.co/dark-amazon-mara/',
            f'Inaccurate link for {LinkType.DARK}')

if __name__ == '__main__':
    unittest.main()
