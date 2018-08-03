from asyncio import AbstractEventLoop
from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup

from extensions.booksearch.bookdata import BookData
from extensions.booksearch.handlers.shamela_handler import ShamelaHandler


def test_init(ctx):
    sh = ShamelaHandler(MagicMock(spec=AbstractEventLoop))

    assert sh.session is not None


def test_process_result_parses_tag_and_returns_bookdata(shamela_bookls1, shamela_bookls2):
    # bookls1, bookls2 are lists of 15 results on the sample pages; static input should give static output.

    test_table = {
        'res/shamela_search_sample.html': shamela_bookls1,
        'res/shamela_search_sample2.html': shamela_bookls2
    }

    for filename, bookls in test_table.items():

        with open(filename, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        results = soup.find_all('td', attrs={'class': "regular-book"})

        sh = ShamelaHandler(MagicMock())
        for index, result in enumerate(results):
            bd = sh.process_result(result)
            assert bd is not None
            bd2 = bookls[index]
            assert bd == bd2


@pytest.mark.asyncio
async def test_search_searches_query(ctx):
    test_table = {
        'الترمذي': 'http://shamela.ws/index.php/search/word/%D8%A7%D9%84%D8%AA%D8%B1%D9%85%D8%B0%D9%8A',
        'ابو داود': 'http://shamela.ws/index.php/search/word/%D8%A7%D8%A8%D9%88+%D8%AF%D8%A7%D9%88%D8%AF',
        'رائد': 'http://shamela.ws/index.php/search/word/%D8%B1%D8%A7%D8%A6%D8%AF',
        'سنن النسائي': ('http://shamela.ws/index.php/search/word/%D8%B3%D9%86%D9%86+'
                        '%D8%A7%D9%84%D9%86%D8%B3%D8%A7%D8%A6%D9%8A'),
        'ابن ماجة': 'http://shamela.ws/index.php/search/word/%D8%A7%D8%A8%D9%86+%D9%85%D8%A7%D8%AC%D8%A9',
        'صحيح مسلم': 'http://shamela.ws/index.php/search/word/%D8%B5%D8%AD%D9%8A%D8%AD+%D9%85%D8%B3%D9%84%D9%85',
        'صحيح البخاري': ('http://shamela.ws/index.php/search/word/%D8%B5%D8%AD%D9%8A%D8%AD+'
                         '%D8%A7%D9%84%D8%A8%D8%AE%D8%A7%D8%B1%D9%8A')
    }

    with open('res/shamela_search_sample.html', 'r', encoding='windows-1256') as f:
        bs = BeautifulSoup(f.read(), 'html.parser')

    async def _fetch(url):
        return bs

    for query, expected_url in test_table.items():
        sh = ShamelaHandler(MagicMock(spec=ctx))
        sh._fetch = _fetch

        results, url = await sh.search(query)
        assert results is not None
        assert url == expected_url

        for result in results:
            assert result is not None
            assert isinstance(result, BookData)
