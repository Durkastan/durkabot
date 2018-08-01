import json

import pytest

from extensions.archive.archive_handler import ArchiveHandler
from extensions.archive.archive_result import ArchiveResult


@pytest.mark.asyncio
async def test_archive_archives_website_returns_result(event_loop):
    ah = ArchiveHandler(event_loop)
    result = await ah.archive('http://www.example.com/')

    assert result is not None
    assert result.link is not None
    assert result.archive_date is not None
    assert result.cache_hit is not None


def test_process_result_returns_archive_result_from_headers():
    test_samples = {
        'res/archive.org_header_sample.json': ArchiveResult(
            link='http://web.archive.org/web/20180801175226/http://www.example.com/',
            archive_date='Wed, 01 Aug 2018 17:52:26 GMT', cache_hit=True),

        'res/archive.org_header_sample2.json': ArchiveResult(
            link='http://web.archive.org/web/20180801182855/http://www.example.net/',
            archive_date='Wed, 01 Aug 2018 18:28:55 GMT', cache_hit=True),

        'res/archive.org_header_sample3.json': ArchiveResult(
            link='http://web.archive.org/web/20180801183420/http://www.example.org/',
            archive_date='Wed, 01 Aug 2018 18:34:20 GMT', cache_hit=False)
    }

    for file, expected in test_samples.items():
        with open(file, 'r') as f:
            actual = ArchiveHandler.process_result(json.load(f))
            assert actual == expected
