"""
    This module is used to test functionality of the app
"""

import unittest
import requests
from MonsterPage import MonsterPage
from PageParser import PageParser
from Rating import Rating
from LinkType import LinkType
from MonsterType import MonsterType
from lxml import html

class SummAutoTests(unittest.TestCase):
    """
        This class tests all of the functionality in the SummAuto application
    """

    TOTAL_MON_COUNT = 482

    PRINT_DETAILS = False

    # def test_parse_next_search_page(self):
    #     """
    #         Make sure we can hit the landing page which contains
    #         all of the monster in default sorting
    #     """

    #     requested_page = 1
    #     end_of_list_parsed = False
    #     all_hrefs = list()

    #     while not end_of_list_parsed:
    #         result = PageParser.parse_next_search_page(requested_page)

    #         for href in result.hrefs:
    #             all_hrefs.append(href)

    #         if result.json_pages == 0:
    #             end_of_list_parsed = True
    #         else:
    #             requested_page += 1

    #     if self.PRINT_DETAILS:
    #         print(f'Done running. Total hrefs: {len(all_hrefs)}')

    #     self.assertEqual(
    #         len(all_hrefs),
    #         self.TOTAL_MON_COUNT,
    #         f'Expected {self.TOTAL_MON_COUNT} hrefs...')

    def test_load_monster_plural_page(self):
        """
            Make sure we can hit the landing page which contains
            all of the monster in default sorting
        """
        page = requests.get('http://summonerswar.co/category/monsters/', headers=PageParser.HEADERS)

        self.assertTrue(page.ok, f'Non-proper page load. Got status code={page.status_code}')

        tree = html.fromstring(page.content)
        hrefs = tree.xpath('//a[@class="layer-link"]/@href')
        self.assertGreater(len(hrefs), 0, 'Expected some hrefs...')

    def test_parse_single_mon_page(self):
        """
            Make sure we can load and parse information from
            a single monster page
        """
        page = requests.get('https://summonerswar.co/dark-amazon-mara/', headers=PageParser.HEADERS)
        self.assertTrue(page.ok, f'Non-proper page load. Got status code={page.status_code}')
        tree = html.fromstring(page.content)
        mon = MonsterPage(tree)

        self.assertEqual(
            mon.sleepy_name,
            'Dark Amazon',
            f'Expected monster sleepy name to equal "Dark Amazon"')
        self.assertEqual(mon.awaken_name, 'Mara', 'Expected monster awakened name to equal "Mara"')

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

        # self.assertEqual(
        #     mon.links[LinkType.IMAGE_SLEEPY],
        #     'https://43ch47qsavx2jcvnr30057vk-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/Amazon_Dark_Icon.png',
        #     'Inaccurate link for image sleepy'
        # )

        # self.assertEqual(
        #     mon.links[LinkType.IMAGE_AWAKE],
        #     'https://43ch47qsavx2jcvnr30057vk-wpengine.netdna-ssl.com/wp-content/uploads/2015/02/Mara_Icon.png',
        #     'Inaccurate link for image awakened'
        # )

        self.assertEqual(
            mon.links[LinkType.DARK],
            '//summonerswar.co/dark-amazon-mara/',
            'Inaccurate link for dark')
        self.assertEqual(
            mon.links[LinkType.FIRE],
            '//summonerswar.co/fire-amazon-ceres/',
            'Inaccurate link for fire')
        self.assertEqual(
            mon.links[LinkType.WATER],
            '//summonerswar.co/water-amazon-ellin/',
            'Inaccurate link for water')
        self.assertEqual(
            mon.links[LinkType.WIND],
            '//summonerswar.co/wind-amazon-hina/',
            'Inaccurate link for wind')
        self.assertEqual(
            mon.links[LinkType.LIGHT],
            '//summonerswar.co/light-amazon-lyn/',
            'Inaccurate link for light')

if __name__ == '__main__':
    unittest.main()
