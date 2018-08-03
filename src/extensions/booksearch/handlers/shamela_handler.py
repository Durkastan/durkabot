from urllib.parse import quote_plus, urljoin

import aiohttp
from bs4 import BeautifulSoup, Tag

from extensions.booksearch.bookdata import BookData


class ShamelaHandler:
    domain = 'http://shamela.ws/'
    search_url = domain + 'index.php/search/word/{0}'
    download_url = 'http://d.shamela.ws/epubs/{0}/{1}.epub'

    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)

    async def _fetch(self, url):
        async with self.session.get(url) as r:
            return BeautifulSoup(await r.text(), 'html.parser')

    async def search(self, query):
        url = self.search_url.format(quote_plus(query))
        soup = await self._fetch(url)

        # shamela is nice :]
        book_elements = soup.find_all('td', attrs={'class': "regular-book"})

        bookdata_instances = [
            self.process_result(result)
            for result in book_elements
        ]

        return bookdata_instances, url

    def process_result(self, result: Tag) -> BookData:
        title_element = result.find_next('a')
        book_title = title_element.string

        relative_link_on_site = title_element['href']
        link_on_site = urljoin(self.domain, relative_link_on_site)

        # extract book id to formulate direct download link
        slash_index = relative_link_on_site.rfind('/')
        book_id = relative_link_on_site[slash_index + 1:]

        # we also need a "fragment" of sorts
        # we drop 2 digits from the end of the id
        # what we have left, which may be 3 or less digits,
        # we left-pad it with 0 until it is 3 digits.
        book_id_fragment = book_id[:-2].rjust(3, '0')

        link = self.download_url.format(book_id_fragment, book_id)

        author_span = result.find_next('span', attrs={'style': "float:left;"})
        author_name = author_span.find_next('a').string

        return BookData(book_title, author_name, link, link_on_site)

    @staticmethod
    def format_result(bookdata):
        title = bookdata.title
        subtext = (
                f"لـ {bookdata.author_name}\n"
                + (f"[---]({bookdata.link}) :الرابط المباشر\n" if bookdata.link is not None else '')
                + (f"[---]({bookdata.site_link}) :الرابط على المكتبة الشاملة\n" if bookdata.site_link is not None else '')
        )
        return title, subtext



