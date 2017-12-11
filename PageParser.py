"""
    This is the Page Parser module
"""

import requests
from SearchPageResult import SearchPageResult

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

    POST_HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) ' +
                      'AppleWebKit/605.1.12 (KHTML, like Gecko) Version/11.1 Safari/605.1.12'
    }

    def parse_next_search_page(self, requested_page, num_requested=25):
        """
            This loads and parses a search page result
        """
        print(f'Requesting page {requested_page}...')
        response = requests.post(
            'https://summonerswar.co/wp-admin/admin-ajax.php',
            headers=PageParser.POST_HEADERS,
            data=self.get_search_page_request(
                page_num=requested_page,
                opts={'articles_num': num_requested}
            )
        )

        if not response.ok:
            raise Exception(f'Err on {requested_page}; status={response.status_code}')

        json = response.json()
        return SearchPageResult(requested_page, json)

    def get_search_page_request(self, page_num=1, opts=None):
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
        articles_num = opts['articles_num']     if 'articles_num' in opts else PageParser.DEFAULT_SEARCH['article_num']
        cols = opts['cols']                     if 'cols' in opts else PageParser.DEFAULT_SEARCH['cols']
        rating = opts['rating']                 if 'rating' in opts else PageParser.DEFAULT_SEARCH['rating']
        sorter = opts['sorter']                 if 'sorter' in opts else PageParser.DEFAULT_SEARCH['sorter']
        category_name = opts['category_name']   if 'category_name' in opts else PageParser.DEFAULT_SEARCH['category_name']
        title = opts['title']                   if 'title' in opts else PageParser.DEFAULT_SEARCH['title']

        data_pieces = [
            'action=itajax-sort&view=grid&loop=main+loop',
            f'&location=&thumbnail=1&rating={rating}&meta=1&award=1&badge=1',
            f'&authorship=1&icon=1&excerpt=1&sorter={sorter}&columns={cols}',
            f'&layout=full&numarticles={articles_num}&paginated={page_num}&largefirst=',
            f'&title={title}&timeperiod=',
            f'&currentquery%5Bcategory_name%5D={category_name}'
        ]
        return ''.join(data_pieces)
