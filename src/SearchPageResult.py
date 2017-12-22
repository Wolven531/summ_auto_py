"""
    This is the SearchPageResult module
"""

from lxml import html

from .ConsoleUtil import ConsoleUtil

class SearchPageResult():
    """
        This class represents the parsed result of a single search
        page
    """

    @classmethod
    def __parse_urls_from_response(cls, target_str):
        """
            This function should grab all URLs from within a blob of text
        """
        tree = html.fromstring(target_str)
        urls = tree.xpath('//a[@class="layer-link"]/@href')
        return urls

    def __init__(self, page, json):
        self.page_num = page
        self.json = json
        self.json_pages = self.json['pages']
        self.json_content = self.json['content']
        self.hrefs = self.__parse_urls_from_response(self.json_content)
        ConsoleUtil.success(f'Parsed {self.page_num}; resp.pages: {self.json_pages}')

    def print_search_info(self):
        """
            This method prints out the basic information parsed from a search page
        """
        ConsoleUtil.info(f'Page Num: {self.page_num}')
        ConsoleUtil.info(f'Href Count: {len(self.hrefs)}')
        ConsoleUtil.info(f'JSON Pages: {len(self.json_pages)}')
