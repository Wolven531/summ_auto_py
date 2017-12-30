"""
    This is the MonsterDownloader module
"""

import json
import os
import requests
import sys

from lxml import html
from src.ConsoleUtil import ConsoleUtil
from src.LinkType import LinkType
from src.MonsterPage import MonsterPage

class MonsterDownloader():
    """
        This class contains functionality for downloading monsters
    """

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

    @staticmethod
    def download_urls(urls):
        """
            This method will attempt to iterate through a list
            of URLs and serialize each as a JSON file
        """
        for url in urls:
            ConsoleUtil.norm(f'Starting URL={url}')
            mon = MonsterDownloader.ensure_mon_load(url, 5)
            mon.serialize()

    @staticmethod
    def download_searched_links(list_of_terms):
        """
            This method will attempt to load the searched link
            JSON file and use it to download and serialize all
            of the monsters on the links within it. Optionally,
            given a list of terms, this will only attempt those
            URLs that contain ANY of the terms
        """
        num_terms = len(list_of_terms)
        data = {'searched_links': []}

        with open(os.getcwd() + '/data/searched_links.json', 'r') as in_file:
            data = json.load(in_file)

        # NOTE: here we filter the list down if we have any list_of_terms
        if num_terms > 0:
            data['searched_links'] = [link for link in data['searched_links'] if any(term in link for term in list_of_terms)]

        MonsterDownloader.download_urls(data['searched_links'])

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

            page = requests.get(url, headers=MonsterDownloader.HEADERS)

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

if __name__ == '__main__':
    num_args = len(sys.argv)
    list_of_terms = []
    if num_args > 1:
        list_of_terms = sys.argv[1:]
    ConsoleUtil.info(f'Downloading searched links (terms={str(list_of_terms)})...')
    MonsterDownloader.download_searched_links(list_of_terms)
    ConsoleUtil.success('Download finished')
