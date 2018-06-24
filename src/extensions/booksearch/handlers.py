from typing import List

import aiohttp
from bs4 import BeautifulSoup, Tag

from extensions.booksearch.bookdata import BookData


class WaqfeyaHandler:
    url = 'http://waqfeya.com/search.php?getword={0}&field={1}'
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
            return BeautifulSoup(await r.text(), 'html.parser')

    async def search(self, query, tag) -> List[BookData]:
        url = self.url.format(query, self.fields.get(tag) or self.fields['tags'])

        soup = await self._fetch(url)

        # There's no concrete way to discern between search results and other table-like elements
        # so we skip the first two and the last one which aren't search elements and
        # hopefully the rest will be. Fragile, I know.
        results = soup.find_all('span', attrs={'class': 'postbody'})[2:-1]

        processed_results = [
            self.process_result(result)
            for result in results
        ]

        return processed_results

    @staticmethod
    def process_result(result: Tag) -> BookData:
        """
        Converts incredibly annoying HTML into BookData

        Args:
            result: Your BeautifulSoup tag

        Returns: A BookData instance of the book in question

        """
        data_table = result.find(name='ul')

        title_tag = data_table.find(name='li')
        title = title_tag.string.replace('&nbsp;', '').split(':', 1)[1].strip()

        category_tag = title_tag.find_next_sibling(name='li')

        author_tag = category_tag.find_next_sibling(name='li')
        author = author_tag.string.replace('&nbsp;', '').split(':', 1)[1].strip()

        verifier_tag = author_tag.find_next_sibling(name='li')
        date_added_tag = verifier_tag.find_next_sibling(name='li')
        seen_counter_tag = date_added_tag.find_next_sibling(name='li')

        download_link_tag = seen_counter_tag.find_next_sibling(name='li').find('a')
        link = download_link_tag.get('href')

        # link on site: this one is a bit tricky
        header_table = result.find_parent(name='table').find_previous_sibling(name='table')
        link_element = header_table.find(name='span', attrs={'class': 'cattitle'}).find(name='a')
        site_link = link_element.get('href')

        return BookData(title, author, link, site_link)
