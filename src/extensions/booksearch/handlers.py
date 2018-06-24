import re
from typing import List, Tuple
from urllib.parse import quote_plus

import aiohttp
from bs4 import BeautifulSoup, Tag

from extensions.booksearch.bookdata import BookData


class WaqfeyaHandler:
    domain = 'http://waqfeya.com/'
    url = domain + 'search.php?getword={0}&field={1}'
    fields = {
        'title': 'btitle',
        'author': 'athid',
        'verifier': 'verid',
        'card': 'binfo',
        'toc': 'btoc',
        'tags': 'btags'  # default
    }

    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)

    async def _fetch(self, url):
        async with self.session.get(url) as r:
            return BeautifulSoup(await r.text(encoding='windows-1256'), 'html.parser', from_encoding='windows-1256')

    async def search(self, query, tag) -> Tuple[List[BookData], str]:
        url = self.url.format(quote_plus(query, encoding='windows-1256'), self.fields.get(tag) or self.fields['tags'])

        soup = await self._fetch(url)

        # There's no concrete way to discern between search results and other table-like elements
        # so we skip the first two and the last one which aren't search elements and
        # hopefully the rest will be. Fragile, I know.
        results = soup.find_all('span', attrs={'class': 'postbody'})[2:-1]

        processed_results = [
            self.process_result(result)
            for result in results
        ]

        return processed_results, url

    def process_result(self, result: Tag) -> BookData:
        """
        Converts incredibly annoying HTML into BookData

        Args:
            result: Your BeautifulSoup tag

        Returns: A BookData instance of the book in question

        """
        title, author, link, site_link = None, None, None, None

        data_table = result.find(name='ul')

        title_tag = data_table.find(text=re.compile('عنوان الكتاب:.*'))
        title = title_tag.string.replace('&nbsp;', '').split(':', 1)[1].strip()

        author_tag = data_table.find(text=re.compile('المؤلف:.*'))
        if author_tag is not None:
            author = author_tag.string.replace('&nbsp;', '').split(':', 1)[1].strip()

        download_text = data_table.find(text=re.compile('رابط التحميل.*'))
        if download_text is not None:
            link = download_text.parent.get('href')

        # link on site: this one is a bit tricky
        header_table = result.find_parent(name='table').find_previous_sibling(name='table')
        link_element = header_table.find(name='span', attrs={'class': 'cattitle'}).find(name='a')
        site_link = self.domain + link_element.get('href')

        return BookData(title, author, link, site_link)
