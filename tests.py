"""
    This module is used to test functionality of the app
"""

import unittest
import requests
from MonsterPage import MonsterPage
from SearchPageResult import SearchPageResult
from lxml import html

def parse_next_search_page(requested_page, num_requested=25):
    """
        This loads and parses a search page result
    """
    print(f'Requesting page {requested_page}...')
    response = requests.post(
        'https://summonerswar.co/wp-admin/admin-ajax.php',
        headers=FuncTests.POST_HEADERS,
        data=get_search_page_request(
            page_num=requested_page,
            opts={'articles_num': num_requested}
        )
    )

    if not response.ok:
        raise Exception(f'Err on {requested_page}; status={response.status_code}')

    json = response.json()
    return SearchPageResult(requested_page, json)

def get_search_page_request(page_num=1, opts=None):
    """
        This function provides the payload data for the next mon request

        Returns:
            string: The payload data with appropriate values substituted in

        Args:
            page_num = 1,
            opts = {
                articles_num = 16
                cols = 1
                rating = 1
                sorter = 'title'
                category_name = 'monsters'
                title = 'Alphabetical+By+Title'
            }
    """
    opts = opts or {}
    articles_num = opts['articles_num']     if 'articles_num' in opts else FuncTests.DEFAULT_SEARCH['article_num']
    cols = opts['cols']                     if 'cols' in opts else FuncTests.DEFAULT_SEARCH['cols']
    rating = opts['rating']                 if 'rating' in opts else FuncTests.DEFAULT_SEARCH['rating']
    sorter = opts['sorter']                 if 'sorter' in opts else FuncTests.DEFAULT_SEARCH['sorter']
    category_name = opts['category_name']   if 'category_name' in opts else FuncTests.DEFAULT_SEARCH['category_name']
    title = opts['title']                   if 'title' in opts else FuncTests.DEFAULT_SEARCH['title']

    data_pieces = [
        'action=itajax-sort&view=grid&loop=main+loop',
        f'&location=&thumbnail=1&rating={rating}&meta=1&award=1&badge=1',
        f'&authorship=1&icon=1&excerpt=1&sorter={sorter}&columns={cols}',
        f'&layout=full&numarticles={articles_num}&paginated={page_num}&largefirst=',
        f'&title={title}&timeperiod=',
        f'&currentquery%5Bcategory_name%5D={category_name}'
    ]
    return ''.join(data_pieces)

class FuncTests(unittest.TestCase):
    """
        Some class docstring
    """

    DEFAULT_SEARCH = {
        'articles_num': 16,
        'cols': 1,
        'rating': 1,
        'sorter': 'title',
        'category_name': 'monsters',
        'title': 'Alphabetical+By+Title'
    }

    HEADERS = {
        # 'Referer': 'https://summonerswar.co/',
        # 'Host': 'summonerswar.co',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Connection': 'keep-alive',
        # 'Accept-Encoding': 'br, gzip, deflate',
        # 'Accept-Language': 'en-us',
        # 'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) ' +
                      'AppleWebKit/605.1.12 (KHTML, like Gecko) Version/11.1 Safari/605.1.12'
    }

    POST_HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) ' +
                      'AppleWebKit/605.1.12 (KHTML, like Gecko) Version/11.1 Safari/605.1.12'
    }

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
    #         result = parse_next_search_page(requested_page)

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
        page = requests.get('http://summonerswar.co/category/monsters/', headers=self.HEADERS)

        self.assertTrue(page.ok, f'Non-proper page load. Got status code={page.status_code}')

        tree = html.fromstring(page.content)
        hrefs = tree.xpath('//a[@class="layer-link"]/@href')
        self.assertGreater(len(hrefs), 0, 'Expected some hrefs...')

    def test_parse_single_mon_page(self):
        """
            Make sure we can load and parse information from
            a single monster page
        """
        page = requests.get('https://summonerswar.co/dark-amazon-mara/', headers=self.HEADERS)
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
