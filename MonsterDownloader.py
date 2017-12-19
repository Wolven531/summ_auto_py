"""
    This is the MonsterDownloader module
"""

import json
import os

from PageParser import PageParser

class MonsterDownloader():
    """
        This class contains functionality for downloading monsters
    """

    @staticmethod
    def download_urls(urls):
        """
            This method will attempt to iterate through a list
            of URLs and serialize each as a JSON file
        """
        for url in urls:
            print(f'Starting URL={url}')
            mon = PageParser.ensure_mon_load(url)
            mon.serialize()

    @staticmethod
    def download_searched_links():
        """
            This method will attempt to load the searched link
            JSON file and use it to download and serialize all
            of the monsters on the links within it
        """
        data = {'searched_links': []}
        with open(os.getcwd() + '/data/searched_links.json', 'r') as in_file:
            data = json.load(in_file)
        MonsterDownloader.download_urls(data['searched_links'])

if __name__ == '__main__':
    print('Downloading searched links...')
    MonsterDownloader.download_searched_links()
    print('Download finished')
