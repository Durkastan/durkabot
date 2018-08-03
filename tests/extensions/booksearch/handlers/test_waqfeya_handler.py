from asyncio import AbstractEventLoop
from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup

from extensions.booksearch.bookdata import BookData
from extensions.booksearch.handlers import WaqfeyaHandler


def test_init():
    wh = WaqfeyaHandler(MagicMock(spec=AbstractEventLoop))

    assert wh.session is not None


def test_process_result_parses_tag_and_returns_bookdata(bookls1, bookls2):
    # bookls1, bookls2 are lists of 15 results on the sample pages; static input should give static output.

    test_table = {
        'res/search_sample.html': bookls1,
        'res/search_sample2.html': bookls2
    }

    for filename, bookls in test_table.items():
        # Notice that the webpages are encoded in windows-1256, which is why we're loading it as such
        with open(filename, 'r', encoding='windows-1256') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        results = soup.find_all('span', attrs={'class': 'postbody'})[2:-1]

        wh = WaqfeyaHandler(MagicMock())
        for index, result in enumerate(results):
            bd = wh.process_result(result)
            assert bd is not None
            bd2 = bookls[index]
            assert bd == bd2
            assert bd.title == bd2.title
            assert bd.author_name == bd2.author_name
            assert bd.link == bd2.link
            assert bd.site_link == bd2.site_link


@pytest.mark.asyncio
async def test_search_searches_query(ctx):
    test_table = {
        ('صحيح البخاري', ''): 'http://waqfeya.com/search.php?'
                              'getword=%D5%CD%ED%CD+%C7%E1%C8%CE%C7%D1%ED&field=btags',
        ('سنن النسائي', 'title'): 'http://waqfeya.com/search.php?'
                                  'getword=%D3%E4%E4+%C7%E1%E4%D3%C7%C6%ED&field=btitle',
        ('الترمذي', 'author'): 'http://waqfeya.com/search.php?getword=%C7%E1%CA%D1%E3%D0%ED&field=athid',
        ('رائد', 'verifier'): 'http://waqfeya.com/search.php?getword=%D1%C7%C6%CF&field=verid',
        ('ابو داود', 'card'): 'http://waqfeya.com/search.php?getword=%C7%C8%E6+%CF%C7%E6%CF&field=binfo',
        ('ابن ماجة', 'toc'): 'http://waqfeya.com/search.php?getword=%C7%C8%E4+%E3%C7%CC%C9&field=btoc',
        ('صحيح مسلم', 'tags'): 'http://waqfeya.com/search.php?getword=%D5%CD%ED%CD+%E3%D3%E1%E3&field=btags'
    }

    with open('res/search_sample.html', 'r', encoding='windows-1256') as f:
        bs = BeautifulSoup(f.read(), 'html.parser')

    async def _fetch(url):
        return bs

    for (query, tag), expected_url in test_table.items():

        wh = WaqfeyaHandler(MagicMock(spec=ctx))
        wh._fetch = _fetch

        results, url = await wh.search(query, tag)
        assert results is not None
        assert url == expected_url

        for result in results:
            assert result is not None
            assert isinstance(result, BookData)
