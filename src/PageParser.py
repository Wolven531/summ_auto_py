"""
    This is the Page Parser module
"""

import json
import os
import requests

from lxml import html
from .ConsoleUtil import ConsoleUtil
from .LinkType import LinkType
from .MonsterPage import MonsterPage
from .SearchPageResult import SearchPageResult

class PageParser():
    """
        This class enables the parsing of a page
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

    TOTAL_MON_COUNT = 482

    PRINT_DETAILS = False

    POST_HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) ' +
                      'AppleWebKit/605.1.12 (KHTML, like Gecko) Version/11.1 Safari/605.1.12'
    }

    @staticmethod
    def ensure_mon_load(url, max_attempts=3):
        """
            This method attempts to ensure a monster page, provided
            by URL, is successfully loaded by retrying up to a max
            number of times (default=3)
        """
        parsed_mon = None
        for attempt in range(1, max_attempts):

            if parsed_mon != None:
                continue

            page = requests.get(url, headers=PageParser.HEADERS)

            if not page.ok:
                ConsoleUtil.warn(f'~~~Attempt {attempt} No page load, retrying {url}')
                continue

            tree = html.fromstring(page.content)
            potential = MonsterPage(tree)
            self_link_type = MonsterPage.convert_element_to_link_type(potential.element)

            if potential.links[LinkType.IMAGE_SLEEPY] == '':
                ConsoleUtil.warn(f'~~~Attempt {attempt} No image, retrying {url}')
                continue

            num_missing_links = 0

            for link in potential.links:
                if potential.links[link] == '':
                    num_missing_links += 1

            if num_missing_links == 5 and attempt == max_attempts - 1:
                ConsoleUtil.warn('~~~Special case, all links were blank, retried max times')
            elif num_missing_links > 2:
                ConsoleUtil.warn(f'~~~Attempt {attempt} Missing at least two links, ' +
                                 f'retrying {url}; had={potential.links}')
                continue

            # attempt a self type fix to minimize runs (if needed)
            if potential.links[self_link_type] == '':
                fixed_url = url.replace('https:', '')
                potential.links[self_link_type] = fixed_url

            parsed_mon = potential

        return parsed_mon

    @staticmethod
    def parse_search_pages(write_to_disk=True):
        """
            This method will attempt to scrape the search API for
            MonsterPage URLs; if called with no param, this method
            will save the results of the scrape to disk; pass False
            to prevent this
            NOTE: this method takes time to complete
        """
        requested_page = 1
        end_of_list_parsed = False
        all_hrefs = list()

        while not end_of_list_parsed:
            result = PageParser.parse_next_search_page(requested_page)

            for href in result.hrefs:
                all_hrefs.append(href)

            if result.json_pages == 0:
                end_of_list_parsed = True
            else:
                requested_page += 1

        if PageParser.PRINT_DETAILS:
            ConsoleUtil.success(f'Done running. Total hrefs: {len(all_hrefs)}')

        data = {
            'count': len(all_hrefs),
            'searched_links': all_hrefs
        }

        if write_to_disk:
            with open(os.getcwd() + '/data/searched_links.json', 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=2)
        return data

    @staticmethod
    def parse_next_search_page(requested_page, num_requested=25):
        """
            This loads and parses a search page result
        """
        ConsoleUtil.info(f'Requesting page {requested_page}...')
        response = requests.post(
            'https://summonerswar.co/wp-admin/admin-ajax.php',
            headers=PageParser.POST_HEADERS,
            data=PageParser.get_search_page_request(
                page_num=requested_page,
                opts={'articles_num': num_requested}
            )
        )

        if not response.ok:
            raise Exception(f'Err on {requested_page}; status={response.status_code}')

        json_resp = response.json()
        return SearchPageResult(requested_page, json_resp)

    @staticmethod
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

        if 'articles_num' in opts:
            articles_num = opts['articles_num']
        else:
            articles_num = PageParser.DEFAULT_SEARCH['article_num']

        if 'cols' in opts:
            cols = opts['cols']
        else:
            cols = PageParser.DEFAULT_SEARCH['cols']

        if 'rating' in opts:
            rating = opts['rating']
        else:
            rating = PageParser.DEFAULT_SEARCH['rating']

        if 'sorter' in opts:
            sorter = opts['sorter']
        else:
            sorter = PageParser.DEFAULT_SEARCH['sorter']

        if 'category_name' in opts:
            category_name = opts['category_name']
        else:
            category_name = PageParser.DEFAULT_SEARCH['category_name']

        if 'title' in opts:
            title = opts['title']
        else:
            title = PageParser.DEFAULT_SEARCH['title']

        data_pieces = [
            'action=itajax-sort&view=grid&loop=main+loop',
            f'&location=&thumbnail=1&rating={rating}&meta=1&award=1&badge=1',
            f'&authorship=1&icon=1&excerpt=1&sorter={sorter}&columns={cols}',
            f'&layout=full&numarticles={articles_num}&paginated={page_num}&largefirst=',
            f'&title={title}&timeperiod=',
            f'&currentquery%5Bcategory_name%5D={category_name}'
        ]
        return ''.join(data_pieces)
