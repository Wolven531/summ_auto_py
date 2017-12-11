"""
    This is the SearchPageResult module
"""

from lxml import html

class SearchPageResult():
    """
        This class represents the parsed result of a single search
        page
    """

    @staticmethod
    def parse_urls_from_response(target_str):
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
        self.hrefs = SearchPageResult.parse_urls_from_response(self.json_content)
        print(f'Parsed {self.page_num}; resp.pages: {self.json_pages}')

    def print_search_info(self):
        """
            This method prints out the basic information parsed from a search page
        """
        print(f'Page Num: {self.page_num}')
        print(f'Href Count: {len(self.hrefs)}')
        print(f'JSON Pages: {len(self.json_pages)}')
