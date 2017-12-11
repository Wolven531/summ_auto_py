"""
    This module is used to test functionality of the app
"""

import unittest
import requests
from MonsterPage import MonsterPage
from PageParser import PageParser
from lxml import html

class SummAutoTests(unittest.TestCase):
    """
        Some class docstring
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

        self.assertEqual(mon.sleepy_name, 'Dark Amazon', f'Expected monster sleepy name to equal "Dark Amazon"')
        self.assertEqual(mon.awaken_name, 'Mara', f'Expected monster awakened name to equal "Mara"')

        self.assertEqual(mon.element, 'Dark', f'Expected monster to be of type "Dark"')

        self.assertEqual(mon.grade, '★★★', f'Expect monster grade to be three stars')
        self.assertEqual(mon.grade_num, 3, f'Expect numeric value of grade to match number of stars')

        self.assertEqual(mon.mon_type, 'Attack', f'Expect monster type to be "Attack"')
        self.assertEqual(mon.get_from, 'Scroll of Light & Darkness, Temple of Wishes', f'Expect monster get from to be "Scroll of Light & Darkness, Temple of Wishes"')
        self.assertEqual(
            mon.when_awakened,
            'Leader Skill: The Attack Power of ally Monsters is increased by 21% in Guild Battles.',
            f'Inaccurate when awakened message')
        self.assertEqual(
            mon.good_for,
            'PvP Offense against reviver comps',
            f'Inaccurate good for message')
        self.assertEqual(
            mon.skillup_info,
            'Worth fully skilling up, but use family skill ups instead of Devilmons',
            f'Inaccurate skillup info message')

        # self.assertEqual(
        #     mon.link_dark,
        #     '',
        #     f'Inaccurate link for dark')
        self.assertEqual(
            mon.link_fire,
            '//summonerswar.co/fire-amazon-ceres/',
            f'Inaccurate link for fire')
        self.assertEqual(
            mon.link_water,
            '//summonerswar.co/water-amazon-ellin/',
            f'Inaccurate link for water')
        self.assertEqual(
            mon.link_wind,
            '//summonerswar.co/wind-amazon-hina/',
            f'Inaccurate link for wind')
        self.assertEqual(
            mon.link_light,
            '//summonerswar.co/light-amazon-lyn/',
            f'Inaccurate link for light')

if __name__ == '__main__':
    unittest.main()
